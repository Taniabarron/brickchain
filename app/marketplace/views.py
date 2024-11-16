from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def marketplace(request):
    response = {}
    return render(request, 'app/marketplace/templates/marketplace.html', response)

def marketplace_resales(request):
    values = {}
    return values

def resale_token(request):
    values = {}
    return values

def offer_token(request):
    values = {}
    return values

def transfer_token(request):
    values = {}
    return values

def detail(request):
    values = {}
    return values