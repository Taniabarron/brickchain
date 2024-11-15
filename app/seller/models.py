from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Property(models.Model):
    title = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    zip_code = models.CharField(max_length=250)
    property_type = models.CharField(max_length=250)
    description = models.CharField(max_length=4000)
    valuation = models.IntegerField(null=True, blank=True)
    tokens = models.IntegerField(null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(null=True, blank=True)
    hast_tx = models.CharField(max_length=250, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    
class PropertyImages(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    path = models.ImageField(upload_to='property/images/')
    timestamp = models.DateTimeField(default=timezone.now)
    
class PropertyDocs(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    path = models.FileField(upload_to='property/pdfs/')
    timestamp = models.DateTimeField(default=timezone.now)
    
class PropertyLand(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    m2 = models.CharField(max_length=250)
    length = models.CharField(max_length=250)
    width = models.CharField(max_length=250)
    timestamp = models.DateTimeField(default=timezone.now)
    
class PropertyBuilding(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    m2_land = models.CharField(max_length=250)
    m2_house = models.CharField(max_length=250)
    age = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    half_baths = models.IntegerField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True) 
    furnished = models.BooleanField(null=True, blank=True)
    garden = models.BooleanField(null=True, blank=True)
    pool = models.BooleanField(null=True, blank=True)
    land_use = models.CharField(max_length=250)
    parking = models.IntegerField(null=True, blank=True)
    services = models.BooleanField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)