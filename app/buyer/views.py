from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app.core.utilis import _decrypt
from app.seller.models import Property

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
    
    response = {}

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