from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app.core.utilis import _decrypt
from app.seller.models import *
from app.buyer.models import Token

@login_required
def tokens(request):
    values = {}
    return values

@login_required
def sales(request):
    values = {}
    return values

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
    
    data.append(
        {
            "Id": token,
            "Title": p.title,
            "Description": p.description,
            "Country": p.country,
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
    
    response = {
         "templates": data,
    }

    return render(request, 'app/buyer/templates/detail.html', response)

@login_required
def buy_token(request):
    values = {}
    return values

@login_required
@csrf_exempt
def get_resale(request):
    values = {}
    return values

@login_required
def cancel_resale(request):
    values = {}
    return values