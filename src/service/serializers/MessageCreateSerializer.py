from rest_framework import serializers

from data import models


class MessageCreateSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset = models.UserProfile.objects.all())
    content = serializers.CharField()
    conversation = serializers.PrimaryKeyRelatedField(queryset = models.Conversation.objects.all())
    
    class Meta:
        model = models.Message
        fields = [
            "sender",
            "content",
            "conversation",
        ]