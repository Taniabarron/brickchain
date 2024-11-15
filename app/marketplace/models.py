from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from app.buyer.models import Token

class Resale(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    publish_price = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(null=True, blank=True)
    auction = models.BooleanField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
class Offers(models.Model):
    resale = models.ForeignKey(Resale, on_delete=models.CASCADE)
    price = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    
class ResaleAnalytics(models.Model):
    resale = models.ForeignKey(Resale, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_resales')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sold_resales')
    hast_tx = models.CharField(max_length=250, null=True, blank=True)
    final_price = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)