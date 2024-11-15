from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from app.seller.models import Property

class Token(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    hast_tx = models.CharField(max_length=250, null=True, blank=True)
    id_chain = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)