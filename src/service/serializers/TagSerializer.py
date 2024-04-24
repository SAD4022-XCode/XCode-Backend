from rest_framework import serializers

from data.models import Tag, TaggedEvent
from .EventSerializer import EventSerializer

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = [
            'label'
        ]

class TaggedItemSerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    event = EventSerializer()
    
    class Meta:
        model = TaggedEvent
        fields = [
            'tag',
            'event',
        ]