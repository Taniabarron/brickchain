from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from app.core.models import Country
from app.core.utilis import _encrypt
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
    values = {}
    return values

@login_required
def resale_token(request):
    values = {}
    return values

@login_required
def offer_token(request):
    values = {}
    return values

@login_required
def transfer_token(request):
    values = {}
    return values

@login_required
def detail(request):
    values = {}
    return values