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

class CreateEventSerializer(serializers.ModelSerializer):
    remaining_tickets = serializers.IntegerField(read_only = True, required = False)
    url = serializers.URLField(required = False)
    province = serializers.CharField(max_length = 255, required = False)
    city = serializers.CharField(max_length = 255, required = False)
    location_lat = serializers.DecimalField(max_digits = 9, decimal_places = 6, required = False)
    location_lon = serializers.DecimalField(max_digits = 9, decimal_places = 6, required = False)

    class Meta:
        model = models.Event
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
            "url",
            "province",
            "city",
            "address",
            "location_lat",
            "location_lon",
            "photo",
        ]

    # def create(self, validated_data):
    #     event = EventSerializer(data = validated_data)
    #     if (validated_data.get("attendance") == "I"):
    #         in_person_event = InPersonEventSerializer(data = validated_data)
    #         in_person_event.event = event
    #         in_person_event.is_valid(raise_exception = True)
    #         in_person_event.save()
    #     elif (validated_data.get("attendance") == "O"):
    #         online_event = OnlineEventSerializer(data = validated_data, event = event)
    #         online_event.save()
    #     event.save()
    #     return super().create(validated_data)

class OnlineEventSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset = models.Event.objects.all())
    
    class Meta:
        model = models.OnlineEvent
        fields = [
            "event",
            "url",
        ]

class InPersonEventSerializer(serializers.ModelSerializer):
    event = EventSerializer(many = False, partial = True)

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
        event.save()
        in_person_event.save()
        # in_person_event.event = event

#         event_serializer = EventSerializer(validated_data.pop("event"))
#         event_serializer.create(data = validated_data.pop("event"))
#         event_serializer.is_valid(raise_exception = True)
#         event_serializer.save()

#         validated_data["event"] = event_serializer

# #        self.fields["event"] = event_serializer
        
        # return super().create(validated_data)