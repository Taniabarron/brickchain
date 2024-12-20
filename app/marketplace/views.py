from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from app.core.models import Country
from app.core.utilis import _decrypt, _encrypt
from app.core.views import save_logbook
from app.marketplace.models import Offers, Resale, ResaleAnalytics
from app.seller.models import *
from app.buyer.models import Token

@login_required
def marketplace(request):
    land = []
    house = []
    apartment = []
    action = []
    action_unique = []
    for p in Property.objects.all().order_by("-timestamp"):
        if p.status:
            color = "info"
            counter = Token.objects.filter(property=p).count()
            stock = p.tokens - counter 
            image = PropertyImages.objects.filter(property=p).order_by('timestamp').values('path')[:1]
            country = Country.objects.get(code=p.country)
            details = {
                        "Id": _encrypt(p.id),
                        "Title": p.title,
                        "Country": country.name,
                        "Image": image[0]['path'],
                        "CreateDate": p.timestamp.strftime("%d/%m/%Y"),
                        "Color": color,
                        "Address": p.address,
                        "Tokens": p.tokens,
                        "Stock": stock,
                        "Cost": p.cost,
                        "Owner": p.user_id.first_name
                    }
            
            if p.property_type == "Land":
                land.append(details)
            elif p.property_type == "House":
                house.append(details)
            else:
                apartment.append(details)
                
            if p.property_type not in action_unique:
                action_unique.append(p.property_type)
                action.append({'id': p.property_type, 'action': p.property_type})

    response = {
        "land": land,
        "house": house,
        "apartment": apartment,
        "action": action
    }
    return render(request, 'app/marketplace/templates/marketplace.html', response)

@login_required
def marketplace_resales(request):
    land = []
    house = []
    apartment = []
    action = []
    action_unique = []
    for p in Resale.objects.all().order_by("-timestamp"):
        if p.status:
            t = Token.objects.get(id=p.token.id)
            image = PropertyImages.objects.filter(property=t.property).order_by('timestamp').values('path')[:1]
            country = Country.objects.get(code=t.property.country)
            details = {
                        "Id": _encrypt(p.id),
                        "Title": t.property.title,
                        "Country": country.name,
                        "Image": image[0]['path'],
                        "CreateDate": p.timestamp.strftime("%d/%m/%Y"),
                        "Address": t.property.address,
                        "Auction": "Auction!" if p.auction else "Unique price",
                        "Cost": p.publish_price,
                        "Owner": t.user_id.first_name
                    }
            
            if t.property.property_type == "Land":
                land.append(details)
            elif t.property.property_type == "House":
                house.append(details)
            else:
                apartment.append(details)
                
            if t.property.property_type not in action_unique:
                action_unique.append(t.property.property_type)
                action.append({'id': t.property.property_type, 'action': t.property.property_type})

    response = {
        "land": land,
        "house": house,
        "apartment": apartment,
        "action": action
    }
    return render(request, 'app/marketplace/templates/marketplace-resales.html', response)

@login_required
def resale_token(request):
    try:
        data = request.POST
        if data.get('id'):
            token = Token.objects.get(id=_decrypt(data.get('id')))
            resale = Resale.objects.create(token=token,
                                    publish_price=data.get('price'),
                                    status=True,
                                    auction=data.get('auction')) 
            print(resale)
            save_logbook("Resale token.", request.user.id) 
            response = {"code": 200, "msg": "Successful resale!"}
        else:
        
            response = {"code": 401, "msg": "Some of the information contains invalid characters"}
    except Exception as e:
        print(e)
        response = {"code": 500, "msg": "We have not been able to complete your purchase"}
    return JsonResponse(response)

@login_required
def offer_token(request):
    try:
        data = request.POST
        #gas check #blockchain
        
        #validations
        if data.get('id'):
            resale = Resale.objects.get(id=_decrypt(data.get('id')))
            if int(data.get('offer_price')) <= resale.publish_price:
                response = {"code": 401, "msg": "Your offer cannot be lower than the price set by the seller."}
            else:
                resale = Offers.objects.create(resale=resale,
                                        price=data.get('offer_price'),
                                        status=False,
                                        user_id=request.user) 
                    
                save_logbook("Create a offer for one token.", request.user.id) 
                
                #change response
                response = {"code": 200, "msg": "Successful offer!"}
        else:
            response = {"code": 401, "msg": "Some of the information contains invalid characters"}
    except Exception as e:
        print(e)
        response = {"code": 500, "msg": "We have not been able to complete your purchase"}
    return JsonResponse(response)

@login_required
def transfer_token(request):
    try:
        data = request.POST
        print("Datos del formulario:", data)
        if data.get('id'):
            #gas check #blockchain
            
            if data.get('offer'):
                offer = Offers.objects.get(id=_decrypt(data.get('id'))) 
                final_price = offer.price
                buyer = offer.user_id
                seller = offer.resale.token.user_id
                resales = offer.resale
                offer.resale.status = False
                offer.resale.token.status = False
                property = offer.resale.token.property
                offer.resale.save()
                offer.resale.token.save()
            else:
                resales = Resale.objects.get(id=_decrypt(data.get('id')))
                resales.status = False
                final_price = data.get('final_price')
                buyer = request.user
                seller = resales.token.user_id
                property = resales.token.property
                resales.token.status = False
                resales.token.save()
                resales.save()
            
            #Transferencia Blockchain
            
            hast_tx = "0x111"
            id_chain = 1
            
            analytics = ResaleAnalytics.objects.create(resale=resales,
                                    buyer=buyer,
                                    seller=seller,
                                    hast_tx = hast_tx,
                                    final_price = final_price) 
            
            print(analytics)
            #new token
            new_token = Token.objects.create(property=property,
                                    user_id=buyer,
                                    cost = final_price,
                                    status = True,
                                    hast_tx=hast_tx,
                                    id_chain=id_chain) 
            print(new_token)
                
            save_logbook("Buy a resale token.", request.user.id) 
            
            response = {"code": 200, "msg": "Successful transfer!"}
        else:
            response = {"code": 401, "msg": "Some of the information contains invalid characters"}
        print(response)
    except Exception as e:
        print(e)
        response = {"code": 500, "msg": "We have not been able to complete your purchase"}
    return JsonResponse(response)

@login_required
def detail(request, token):
    data = []
    action = []
    action_unique = []
    auction = []
    p = Resale.objects.get(id=_decrypt(token))
    
    if p.auction:
        val = ""
        valCart = "hidden"
        offers = Offers.objects.filter(resale=p)
        for o in offers:
            auction.append({
                "Id": _encrypt(o.id),
                "User": o.user_id.first_name[0].upper(),
                "Price": o.price,
                "OfferDate": o.timestamp
            })
    else:
        val = 'hidden'
        valCart = ""
    
    image = PropertyImages.objects.filter(property=p.token.property).order_by('timestamp').values('path')[:1]
    country = Country.objects.get(code=p.token.property.country)

    data.append(
        {
            "Id": _encrypt(p.id),
            "Title": p.token.property.title,
            "Description": p.token.property.description,
            "Country": country.name,
            "Quintaty": 1,
            "Image": image[0]['path'],
            "CreateDate": p.timestamp.strftime("%d/%m/%Y"),
            "Status": val,
            "SuperState": "" if p.status else "hidden",
            "ButtonState": "" if p.token.user_id.id == request.user.id else "hidden",
            "StatusCart": valCart,
            "Address": p.token.property.address,
            "Seller": p.token.user_id.first_name,
            "Cost": p.publish_price,
            "Type": p.token.property.property_type,
        }
    )
    
    if p.token.property.property_type not in action_unique:
        action_unique.append(p.token.property.property_type)
        action.append({'id': p.token.property.property_type, 'action': p.token.property.property_type})
    
    response = {
         "templates": data,
         "action": action,
         "auction": auction
    }

    return render(request, 'app/marketplace/templates/detail.html', response)