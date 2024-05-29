from rest_framework import serializers

from data import models

class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.PrimaryKeyRelatedField(queryset = models.UserProfile.objects.all())

    class Meta:
        model = models.Notification

        fields = [
            "id",
            "recipient",
            "title",
            "content",
            "created_at",
            "is_read",
        ]