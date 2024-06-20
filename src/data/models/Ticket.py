from django.db import models

from data import models as AppModels

class Ticket(models.Model):
    attendee = models.ForeignKey(AppModels.UserProfile, on_delete = models.CASCADE)
    attendee_name = models.CharField(max_length = 255)
    attendee_email = models.EmailField()
    attendee_phone = models.CharField(max_length = 15)
    price = models.IntegerField()
    event = models.ForeignKey(AppModels.Event, on_delete = models.CASCADE)