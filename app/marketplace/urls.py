from django.urls import path
from app.marketplace.views import *

app_name = 'app.marketplace'

urlpatterns = [
    path('marketplace', marketplace, name='marketplace'),
    path('marketplace/list', marketplace_resales, name='marketplace_resales'),
    path('marketplace/resale', resale_token, name='resale_token'),
    path('marketplace/offer', offer_token, name='offer_token'),
    path('marketplace/transfer', transfer_token, name='transfer_token'),
    path('marketplace/detail/<str:token>', detail, name='detail'),
]