from django.urls import path
from app.seller.views import *

app_name = 'app.seller'

urlpatterns = [
    path('seller/properties', properties, name='properties'),
    path('seller/status', status_properties, name='status_properties'),
    path('seller/form/property', form_properties, name='form_properties'),
    path('seller/add/property', add_properties, name='add_properties'),
]