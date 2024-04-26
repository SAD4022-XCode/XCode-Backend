from rest_framework import serializers

from data import models

class EventSerializer(serializers.ModelSerializer):
    remaining_tickets = serializers.IntegerField(read_only = True, required = False)
    id = serializers.IntegerField(read_only = True)
    creator_id = serializers.PrimaryKeyRelatedField(queryset = models.User.objects.all(), required = False)

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
        ]

class EventInfoSerializer(serializers.Serializer):
    event = EventSerializer(read_only = True)
    url = serializers.URLField(required = False)
    province = serializers.CharField(max_length = 255, required = False)
    city = serializers.CharField(max_length = 255, required = False)
    address = serializers.CharField(max_length = 255, required = False)
    location_lat = serializers.DecimalField(max_digits = 9, decimal_places = 6, required = False)
    location_lon = serializers.DecimalField(max_digits = 9, decimal_places = 6, required = False)



class CreateEventSerializer(serializers.ModelSerializer):
    event = EventSerializer(partial = True, many = False)
    url = serializers.URLField(required = False)
    province = serializers.CharField(max_length = 255, required = False)
    city = serializers.CharField(max_length = 255, required = False)
    address = serializers.CharField(max_length = 255)
    location_lat = serializers.DecimalField(max_digits = 9, decimal_places = 6, required = False)
    location_lon = serializers.DecimalField(max_digits = 9, decimal_places = 6, required = False)

    class Meta:
        model = models.Event
        fields = [
            "event",
            "url",
            "province",
            "city",
            "address",
            "location_lat",
            "location_lon",
        ]
    
class OnlineEventSerializer(serializers.ModelSerializer):
    event = EventSerializer(many = False)
    
    class Meta:
        model = models.OnlineEvent
        fields = [
            "event",
            "url",
        ]

    def create(self, validated_data):
        event_data = validated_data.pop("event")
        event = models.Event.objects.create(creator_id = self.context.get("user_id"), **event_data)

        in_person_event = models.OnlineEvent.objects.create(event = event, **validated_data)
        event.save()
        in_person_event.save()

class InPersonEventSerializer(serializers.ModelSerializer):
    event = EventSerializer(partial = True)

    class Meta:
        model = models.InPersonEvent
        fields = [
            "event",
            "province",
            "city",
            "address",
            "location_lat",
            "location_lon",
        ]

    def create(self, validated_data):
        event_data = validated_data.pop("event")
        event = models.Event.objects.create(creator_id = self.context.get("user_id"), **event_data)

        in_person_event = models.InPersonEvent.objects.create(event = event, **validated_data)  

        return in_person_event