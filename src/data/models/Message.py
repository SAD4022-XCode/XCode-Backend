from django.db import models

from data import models as AppModels

class Message(models.Model):
    sender = models.ForeignKey(AppModels.User, on_delete = models.CASCADE)
    conversation = models.ForeignKey(AppModels.Conversation, on_delete = models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)