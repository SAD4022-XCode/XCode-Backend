from rest_framework import serializers

from data.models import EventTag

class EventTagSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(max_length = 255, required = False)

    class Meta:
        model = EventTag
        fields = [
            'tag',
        ]

    def create(self, validated_data):
        new_tag = EventTag.objects.create(event_id = self.context.get("event_id"), **validated_data)

        return new_tag