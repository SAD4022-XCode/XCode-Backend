from rest_framework import serializers

from data.models import Event, InPersonEvent, OnlineEvent

class EventSerializer(serializers.ModelSerializer):
    remaining_tickets = serializers.IntegerField(read_only = True, required = False)

    class Meta:
        model = Event
        fields = [
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
        ]

class OnlineEventSerializer(serializers.ModelSerializer):
    event = EventSerializer(many = False, partial = True)
    
    class Meta:
        model = OnlineEvent
        fields = [
            "event",
            "url",
        ]

class InPersonEventSerializer(serializers.ModelSerializer):
    event = EventSerializer(many = False, partial = True)

    class Meta:
        model = InPersonEvent
        fields = [
            "event",
            "province",
            "city",
            "location_lat",
            "location_lon",
        ]