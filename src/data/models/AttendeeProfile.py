from django.db import models
from django.conf import settings
from .ProfileBase import ProfileBase

class AttendeeProfile(models.Model, ProfileBase):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key = True)
    birth_date = models.DateField(null = True)