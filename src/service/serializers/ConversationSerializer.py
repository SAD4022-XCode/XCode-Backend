from rest_framework import serializers

from data import models
from service import serializers as AppSerializers

class ConversationSerializer(serializers.ModelSerializer):
    participants = AppSerializers.MyUserSerializer(source = "participants")

    class Meta:
        model = models.Conversation
        fields = [
            "created_at",
            "participants",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        last_message = models.Message.objects \
            .filter(conversation_id = instance.id) \
            .last()
        representation["last_message"] = last_message

        return representation