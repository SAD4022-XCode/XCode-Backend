from django.db import models

class EventTagManager(models.Manager):
    def get_tags_for_event(self, event_id):
        return super().get_queryset().filter(event_id = event_id)