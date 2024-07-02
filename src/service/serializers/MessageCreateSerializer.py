from rest_framework import serializers

from data import models

class MessageCreateSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset = models.User.objects.all())
    recipient = serializers.PrimaryKeyRelatedField(read_only = True)
    content = serializers.CharField()
    conversation = serializers.PrimaryKeyRelatedField(queryset = models.Conversation.objects.all(), required = False)
    
    class Meta:
        model = models.Message
        fields = [
            "sender",
            "recipient",
            "content",
            "conversation",
        ]