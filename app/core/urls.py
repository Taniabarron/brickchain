from django.urls import path
from app.core.views import *

app_name = 'app.core'

urlpatterns = [
    path('', index, name='index'),
    path('login', sing_in, name='sing_in'),
    path('core/account/create', account_create, name='account_create'),
    path('core/account/authenticate', user_authenticate, name='authenticate'),
    path('core/account/logout', logout, name='logout'),
    path('core/account/verify/<str:token>', user_verify, name='user_verify'),
    path('core/reset_password/check', reset_password_send, name='reset_password_send'),
    path('core/reset_password/change/<str:token>', change_password, name='change_password'),
    path('core/reset_password/confirm', reset_password, name='reset_password'),
    path('homes', test, name='test'),
    
    path('core/account/logbook', logbook, name='logbook'),
    path('core/account/get_logbook', get_logbook, name='get_logbook'),
    
]