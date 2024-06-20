from django.db import models

from data.models import User
from data.models.Tag import Tag

ATTENDANCE_CHOICES = [
    ('I', 'InPerson'),
    ('O', 'Online'),
]

class Event(models.Model):
    creator = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    category = models.CharField(max_length = 255)
    description = models.TextField()
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    attendance = models.CharField(max_length = 1, choices = ATTENDANCE_CHOICES)
    maximum_tickets = models.IntegerField()
    registered_tickets = models.IntegerField(default = 0)
    is_paid = models.BooleanField(default = False)
    ticket_price = models.IntegerField(null = True)
    organizer_phone = models.CharField(max_length = 11)
    organizer_SSN = models.CharField(max_length = 11)
    tags = models.ManyToManyField(Tag)
    photo = models.ImageField(upload_to = "events/", blank = True, null = True)
    
    @property
    def remaining_tickets(self):
        return self.maximum_tickets - self.registered_tickets
    
    @property
    def start_date(self):
        return self.starts.date()