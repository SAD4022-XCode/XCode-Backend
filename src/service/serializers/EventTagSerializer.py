from rest_framework import serializers

from data.models import EventTag, Event
from .EventSerializer import EventSerializer

class EventTagSerializer(serializers.ModelSerializer):
    # event = serializers.PrimaryKeyRelatedField(queryset = Event.objects.all(), required = False)
    tag = serializers.CharField(max_length = 255, required = False)

    class Meta:
        model = EventTag
        fields = [
            'tag',
        ]

    def create(self, validated_data):
        for tag in validated_data.values:
            new_tag = EventTag.objects.create(tag = tag, event_id = self.context.get("event_id"))
            new_tag.save()  
        # return super().create(validated_data)