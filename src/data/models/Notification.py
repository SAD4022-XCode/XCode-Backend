from django.db import models

from data import models as AppModels

class Notification(models.Model):
    recipient = models.ForeignKey(AppModels.UserProfile,
                                  on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length = 255)
    content = models.TextField()
    is_read = models.BooleanField(default = False)