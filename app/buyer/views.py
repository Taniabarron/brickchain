from datetime import timedelta
from itertools import groupby
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app.core.models import Country
from app.core.utilis import _decrypt, _encrypt
from app.core.views import save_logbook
from app.marketplace.models import Resale
from app.seller.models import *
from app.buyer.models import Token

@login_required
def tokens(request):
    data = []
    action = []
    action_unique = []
    for t in Token.objects.filter(user_id=request.user).order_by("-timestamp"):
        if t.status:
            p = Property.objects.get(id=t.property.id)
            if Resale.objects.filter(token=t.id).exists():
                val = "Resale"
                color = "warning"
            else:
                val = "Active"
                color = "success"
            image = PropertyImages.objects.filter(property=p).order_by('timestamp').values('path')[:1]
            country = Country.objects.get(code=p.country)
            data.append(
                {
                    "Id": _encrypt(t.id),
                    "Title": p.title,
                    "Country": country.name,
                    "Image": image[0]['path'],
                    "CreateDate": p.timestamp.strftime("%d/%m/%Y"),
                    "Status": val,
                    "Color": color,
                    "Address": p.address,
                    "Tokens": p.tokens,
                    "Cost": p.cost,
                    "Type": p.property_type,
                }
            )
            if p.property_type not in action_unique:
                action_unique.append(p.property_type)
                action.append({'id': p.property_type, 'action': p.property_type})
                
        response = {
            "templates": data,
            "action": action
        }
    return render(request, 'app/buyer/templates/my-tokens.html', response)

@login_required
def sales(request):
    return render(request, 'app/buyer/templates/my-sales.html')

@login_required
def detail(request, token):
    data = []
    action = []
    action_unique = []
    token_summary = []
    p = Property.objects.get(id=_decrypt(token))
    image = PropertyImages.objects.filter(property=p).order_by('timestamp').values('path')[:1]
    counter = Token.objects.filter(property=p).count()
    stock = p.tokens - counter 
    sales = counter * p.cost
    country = Country.objects.get(code=p.country)

    data.append(
        {
            "Id": token,
            "Title": p.title,
            "Description": p.description,
            "Country": country.name,
            "Image": image[0]['path'],
            "CreateDate": p.timestamp.strftime("%d/%m/%Y"),
            "Status": "hidden" if stock == 0 else "",
            "Address": p.address,
            "Tokens": p.tokens,
            "Cost": p.cost,
            "Type": p.property_type,
            "Sales": sales,
            "Stock": stock,
            "Items": counter,
        }
    )
    
    if p.property_type not in action_unique:
        action_unique.append(p.property_type)
        action.append({'id': p.property_type, 'action': p.property_type})
    
    
    tokens = Token.objects.filter(property=p).order_by("-timestamp")

    for user_id, user_tokens in groupby(tokens, key=lambda t: t.user_id):
            user_tokens = list(user_tokens)  
            count = len(user_tokens)  
            last_token = user_tokens[0] 

            time_diff = timezone.now() - last_token.timestamp
            if time_diff < timedelta(minutes=1):
                time_ago = "less than a minute ago"
            elif time_diff < timedelta(hours=1):
                minutes = time_diff.seconds // 60
                time_ago = f"{minutes} min ago"
            elif time_diff < timedelta(days=1):
                hours = time_diff.seconds // 3600
                time_ago = f"{hours} hours ago"
            else:
                days = time_diff.days
                time_ago = f"{days} days ago"

            token_summary.append({
                "Initial": user_id.first_name[0].upper(),
                "Msg": " Purchased "+str(count)+" tokens "+ time_ago,
            })
    
    response = {
         "templates": data,
         "list": token_summary,
         "action": action
    }

    return render(request, 'app/buyer/templates/detail.html', response)

@login_required
def buy_token(request):
    try:
        data = request.POST
        
        #gas check #blockchain
        
        hast_tx = "0x000000"
        id_chain = 1
        if data.get('quantity'):
            quantity = int(data.get('quantity'))
            property = Property.objects.get(id=_decrypt(data.get('id')))
            for q in range(quantity):
                #Blockchain
                
                token = Token.objects.create(property=property,
                                    user_id=request.user,
                                    cost = property.cost,
                                    status = True,
                                    hast_tx=hast_tx,
                                    id_chain=id_chain) 
                
            save_logbook("Buy token.", request.user.id) 
            
            response = {"code": 200, "msg": "Successful purchase!"}
        else:
            response = {"code": 401, "msg": "Some of the information contains invalid characters"}
    except Exception as e:
        print(e)
        response = {"code": 500, "msg": "We have not been able to complete your purchase"}
    return JsonResponse(response)   

@login_required
@csrf_exempt
def get_resale(request):
    list = Token.objects.filter(resale__isnull=False, user_id=request.user.id).distinct()
    size = len(list)
    response = {"meta": {
        "page": 1,
        "pages": size / 10,
        "perpage": -1,
        "total": size,
        "sort": "asc",
        "field": "RecordID"}
    }
    data = []
    for r in list:
        resale_status = r.resale_set.first().status if r.resale_set.exists() else None
        publish_price = r.resale_set.first().publish_price if r.resale_set.exists() else None
        action = r.resale_set.first().auction if r.resale_set.exists() else None
        data.append({'RecordID': r.resale_set.first().id,
                     'ResaleID': _encrypt(r.resale_set.first().id),
                     'Property': r.property.title,
                     'Cost': r.property.cost,
                     'Publish': publish_price,
                     'IdChain': r.id_chain,
                     'Auction': "Active" if action else "Desactive",
                     'Status': "Open" if resale_status else "Close",
                     'Action': "" if resale_status else "hidden",
                     'ShipDate': r.timestamp})
    response.update({'data': data})
    return JsonResponse(response)

@login_required
def cancel_resale(request):
    try:
        data = request.POST
        #validations
        if data.get('id'):
            print(data.get('id'))
            resale = Resale.objects.get(id=data.get('id'))
            resale.delete()
            
            save_logbook("Cancel a resale.", request.user.id) 
            
            response = {"code": 200, "msg": "Chage status successful!"}
        else:
            response = {"code": 401, "msg": "Some of the information contains invalid characters"}
    except Exception as e:
        print(e)
        response = {"code": 500, "msg": "We have not been able to complete your offer"}
    return JsonResponse(response)