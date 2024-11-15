from django.urls import path
from app.buyer.views import *

app_name = 'app.buyer'

urlpatterns = [
    path('buyer/tokens', tokens, name='tokens'),
    path('buyer/sales', sales, name='sales'),
    path('buyer/detail/<str:token>', detail, name='detail'),
    path('buyer/buy', buy_token, name='buy_token'),
    path('buyer/get_resale', get_resale, name='get_resale'),
    path('buyer/cancel/resale', cancel_resale, name='cancel_resale'),
]