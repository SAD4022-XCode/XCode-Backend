from django.db import models

from data import models as AppModels

class EventBookmark(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(AppModels.UserProfile, on_delete = models.CASCADE)
    event = models.ForeignKey(AppModels.Event, on_delete = models.CASCADE)