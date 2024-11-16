from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.TextField(verbose_name="Phone", blank=True, null=True)
    terms = models.BooleanField(verbose_name="TermsandConditions", blank=True, null=True)
    img_profile = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.CharField(max_length=100, blank=True, null=True)
    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)
    token_pass = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)
    account_status = models.BooleanField()
    
class Logbook(models.Model):
    action = models.CharField(max_length=250)
    user_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=3, unique=True)