from rest_framework import serializers

from data import models

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset = models.User.objects.select_related("userprofile").all())
    sender_name = serializers.CharField(source = "sender.first_name")
    sender_profile_photo = serializers.ImageField(source = "sender.userprofile.profile_picture")
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

