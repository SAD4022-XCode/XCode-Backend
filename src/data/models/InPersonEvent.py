from django.db import models

from data import models as AppModels

class InPersonEvent(models.Model):
    event = models.OneToOneField(AppModels.Event, 
                                 on_delete = models.CASCADE, 
                                 primary_key = True)
    province = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    address = models.CharField(max_length = 255)
    location_lat = models.DecimalField(max_digits = 17, decimal_places = 15)
    location_lon = models.DecimalField(max_digits = 18, decimal_places = 15)
