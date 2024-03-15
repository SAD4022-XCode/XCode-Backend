from django.db import models
from django.conf import settings

class ProfileBase():
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key = True)