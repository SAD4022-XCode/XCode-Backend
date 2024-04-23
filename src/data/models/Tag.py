from django.db import models
from data.models import Event

class Tag(models.Model):
    label = models.CharField(max_length = 255)

class TaggedEvent(models.Model):
    tag = models.ForeignKey(Tag, on_delete = models.CASCADE)
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
