from django.db import models 

class Conversation(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)