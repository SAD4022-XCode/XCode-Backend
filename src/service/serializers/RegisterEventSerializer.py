from rest_framework import serializers

from data import models

class RegisterEventSerializer(serializers.ModelSerializer):

    registered_events = serializers.JSONField()
    bookmarked_events = serializers.JSONField()
    class Meta:
        model = models.UserProfile
        fields = [
            'registered_events',
            'has_registered',
            'bookmarked_events',
        ]
