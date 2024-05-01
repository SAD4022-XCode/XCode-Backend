from rest_framework import serializers

from data import models

class OnlineEventSerializer(serializers.ModelSerializer):
    # event = EventSerializer(many = False)
    
    class Meta:
        model = models.OnlineEvent
        fields = [
            "url",
        ]

    def create(self, validated_data):
        online_event = models.OnlineEvent.objects.create(event_id = self.context.get("event_id"), 
                                                         **validated_data)
        return online_event
