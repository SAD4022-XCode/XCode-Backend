from django.db import models

from data.models.Event import Event
from data.models.managers import EventTagManager

class EventTag(models.Model):
    tag = models.CharField(max_length = 255)
    event = models.ForeignKey(Event, on_delete = models.CASCADE)

    objects = EventTagManager()
