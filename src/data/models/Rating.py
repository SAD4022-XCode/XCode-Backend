from django.db import models

from data import models as AppModels

RATING_CHOICES = [
    (1, "one star"),
    (2, "two stars"),
    (3, "three stars"),
    (4, "four stars"),
    (5, "five stars"),
]

class Rating(models.Model):
    event = models.ForeignKey(AppModels.Event, on_delete = models.CASCADE)
    user = models.ForeignKey(AppModels.User, on_delete = models.CASCADE)

    score = models.IntegerField(choices = RATING_CHOICES)