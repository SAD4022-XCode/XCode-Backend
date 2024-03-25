from django.db import models
from django.conf import settings
from pathlib import Path

GENDER_MALE = 'M'
GENDER_FEMALE = 'F'
GENDER_UNKNOWN = 'X'

GENDER_CHOICES = [
    (GENDER_MALE, 'Male'),
    (GENDER_FEMALE, 'Female'),
    (GENDER_UNKNOWN, 'Rather not say')
]

def upload_path(instance, filename):
    return Path.joinpath('images', f'{filename}')

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key = True)
    birth_date = models.DateField(null = True)
    city = models.CharField(max_length = 255, blank = True)
    profile_picture = models.ImageField(upload_to = upload_path, blank = True, null = True)
    gender = models.CharField(max_length = 1, 
                              choices = GENDER_CHOICES, 
                              default = GENDER_UNKNOWN)