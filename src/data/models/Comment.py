from django.db import models

from data import models as AppModels

class Comment(models.Model):
    user = models.ForeignKey(AppModels.User, 
                             on_delete = models.CASCADE,
                             related_name = "comments")
    event = models.ForeignKey(AppModels.Event, 
                              on_delete = models.CASCADE,
                              related_name = "comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    score = models.IntegerField(default = 0)
    parent = models.ForeignKey("self",
                                    on_delete = models.CASCADE,
                                    null = True,
                                    blank = True,
                                    related_name = "children")
    