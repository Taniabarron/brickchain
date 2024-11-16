from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from app.core.models import Country
from app.core.utilis import _encrypt
from app.seller.models import *
from app.buyer.models import Token

@login_required
def marketplace(request):
    land = []
    for p in Property.objects.all().order_by("-timestamp"):
        if p.status:
            color = "info"
            counter = Token.objects.filter(property=p).count()
            print(counter)
            stock = p.tokens - counter 
            print(stock)
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
    
    response = {
        "land": land,
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