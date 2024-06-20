from django.db import models

from data import models as AppModels

class OnlineEvent(models.Model):
    event = models.OneToOneField(AppModels.Event, 
                                 on_delete = models.CASCADE,
                                 primary_key = True)
    url = models.URLField()