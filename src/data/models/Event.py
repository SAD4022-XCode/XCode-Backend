from django.db import models
from django.core import validators

ATTENDANCE_CHOICES = [
    ('I', 'InPerson'),
    ('O', 'Online'),
]

class Event(models.Model):
    title = models.CharField(max_length = 255)
    category = models.CharField(max_length = 255)
    description = models.TextField()
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    attendance = models.CharField(max_length = 1, choices = ATTENDANCE_CHOICES)
    maximum_tickets = models.IntegerField()
    registered_tickets = models.IntegerField(default = 0,
                                             validators = [
                                                 validators.MaxValueValidator(maximum_tickets),
                                                 validators.MinValueValidator(0),
                                             ])
    is_paid = models.BooleanField(default = False)
    ticket_price = models.DecimalField(max_digits = 6, decimal_places = 2, null = True)
    organizer_phone = models.CharField(max_length = 11) # + Validation
    organizer_SSN = models.CharField(max_length = 11)
    photo = models.ImageField(upload_to = "events/", blank = True, null = True)
    
    # start_time = models.TimeField()
    # ending_time = models.TimeField()

    @property
    def remaining_tickets(self):
        return self.maximum_tickets - self.registered_tickets

class InPersonEvent(models.Model):
    event = models.OneToOneField(Event, 
                                 on_delete = models.CASCADE, 
                                 primary_key = True)
    province = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    location_lat = models.DecimalField(max_digits = 9, decimal_places = 6)
    location_lon = models.DecimalField(max_digits = 9, decimal_places = 6)

class OnlineEvent(models.Model):
    event = models.OneToOneField(Event, 
                                 on_delete = models.CASCADE,
                                 primary_key = True)
    url = models.URLField()