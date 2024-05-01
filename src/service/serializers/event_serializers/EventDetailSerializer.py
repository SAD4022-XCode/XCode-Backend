from rest_framework import serializers

from service.serializers.event_serializers.EventSerializer import EventSerializer
from service.serializers.event_serializers.InPersonEventSerializer import InPersonEventSerializer
from service.serializers.event_serializers.OnlineEventSerializer import OnlineEventSerializer

from service.serializers import EventTagSerializer

from data import models

class EventDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    creator_id = serializers.PrimaryKeyRelatedField(queryset = models.User.objects.all(), required = False)
    remaining_tickets = serializers.IntegerField(read_only = True, required = False)
    inpersonevent = InPersonEventSerializer()
    onlineevent = OnlineEventSerializer()

    class Meta:
        model = models.Event
        fields = [
            "creator_id",
            "id",
            "title",
            "category",
            "description",
            "starts",
            "ends",
            "attendance",
            "maximum_tickets",
            "remaining_tickets",
            "is_paid",
            "ticket_price",
            "organizer_phone",
            "organizer_SSN",
            "photo",
            "onlineevent",
            "inpersonevent",

        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        tags = models.EventTag.objects.get_tags_for_event(instance.id)
        from service.serializers import EventTagSerializer

        serializer = EventTagSerializer(tags, many = True)
        representation["tags"] = serializer.data

        return representation

