from django.db import models
from django.conf import settings
from django.core import exceptions
from pathlib import Path

from data.models.managers import UserProfileManager
from data.models.Event import Event

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
    ssn = models.CharField(max_length = 10, blank = True)
    phone = models.CharField(max_length = 15, blank = True)
    balance = models.PositiveIntegerField(default = 0)
    birth_date = models.DateField(null = True)
    city = models.CharField(max_length = 255, blank = True)
    province = models.CharField(max_length = 255, blank = True)
    profile_picture = models.ImageField(upload_to = 'images/', blank = True, null = True)
    gender = models.CharField(max_length = 1, 
                              choices = GENDER_CHOICES, 
                              default = GENDER_UNKNOWN)
    enrolled_events = models.ManyToManyField(Event, through = "Ticket")
    has_enrolled = models.BooleanField(default = False)
    
    objects = UserProfileManager()

    def get_profile_picture(self):
        return self.profile_picture.file
    
    def delete_profile_picture(self):
        self.profile_picture.delete(save = True)

    def pay(self, price):
        if (self.balance < price):
            raise exceptions.BadRequest
        self.balance -= price
        return self.balance
    
    def deposit(self, value):
        self.balance += value
        return self.balance
