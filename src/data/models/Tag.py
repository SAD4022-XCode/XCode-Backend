from django.db import models

from data.models.managers import EventTagManager

class Tag(models.Model):
    label = models.CharField(max_length = 255)

    objects = EventTagManager()

    def __str__(self) -> str:
        return self.label
