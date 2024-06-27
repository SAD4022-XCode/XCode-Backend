from django.db import models

from data import models as AppModels


class UserConversation(models.Model):
    user = models.ForeignKey(AppModels.User, on_delete = models.CASCADE)
    conversation = models.ForeignKey(AppModels.Conversation, on_delete = models.CASCADE)