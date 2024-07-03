from rest_framework import serializers

from data import models

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset = models.UserProfile.objects.select_related("user").all())
    sender_name = serializers.CharField(source = "sender.user.first_name")
    sender_profile_photo = serializers.ImageField(source = "sender.profile_picture")
    conversation = serializers.PrimaryKeyRelatedField(queryset = models.Conversation.objects.all())

    class Meta:
        model = models.Message
        fields = [
            "sender",
            "sender_name",
            "sender_profile_photo",
            "conversation",
            "content",
            "timestamp",
            "is_read",
        ]

