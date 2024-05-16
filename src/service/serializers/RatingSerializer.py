from rest_framework import serializers

from data import models
from data.models.Rating import RATING_CHOICES

class RatingSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset = models.Event.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset = models.User.objects.all())
    score = serializers.ChoiceField(choices = RATING_CHOICES)

    class Meta: 
        model = models.Rating
        fields = [
            "event",
            "user",
            "score",
        ]