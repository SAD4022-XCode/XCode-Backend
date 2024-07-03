from rest_framework import serializers

from data import models

class MessageCreateInputSerializer(serializers.Serializer):
    recipient = serializers.PrimaryKeyRelatedField(queryset = models.UserProfile.objects.all())
    content = serializers.CharField()
    