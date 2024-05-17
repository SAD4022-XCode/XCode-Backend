from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from pathlib import Path

from .managers import UserProfileManager

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
    province = models.CharField(max_length = 255, blank = True)
    profile_picture = models.ImageField(upload_to = 'images/', blank = True, null = True)
    wallet = models.IntegerField(default = 0, validators = [MinValueValidator(0)])
    gender = models.CharField(max_length = 1, 
                              choices = GENDER_CHOICES, 
                              default = GENDER_UNKNOWN)
    registered_events = models.JSONField(encoder = None, decoder = None)
    bookmarked_events = models.JSONField(encoder = None, decoder = None)
    
    objects = UserProfileManager()

    def get_profile_picture(self):
        return self.profile_picture.file
    
    def delete_profile_picture(self):
        self.profile_picture.delete(save = True)