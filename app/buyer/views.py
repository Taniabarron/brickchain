from datetime import timedelta
from itertools import groupby
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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
        print(data)
        #change response
        response = {"code": 200, "msg": "Successful purchase!"}
    except Exception as e:
        print(e)
        response = {"code": 500, "msg": "We have not been able to complete your purchase"}
    return JsonResponse(response)   

@login_required
@csrf_exempt
def get_resale(request):
    values = {}
    return values

@login_required
def cancel_resale(request):
    values = {}
    return values