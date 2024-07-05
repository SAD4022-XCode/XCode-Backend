from rest_framework import serializers

from service.serializers.event_serializers.InPersonEventSerializer import InPersonEventSerializer
from service.serializers.event_serializers.OnlineEventSerializer import OnlineEventSerializer
from data import models

class EventDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    creator_id = serializers.PrimaryKeyRelatedField(queryset = models.User.objects.all(), required = False)
    organizer_name = serializers.CharField(source = "creator.first_name")
    organizer_photo = serializers.ImageField(source = "creator.userprofile.profile_picture")
    organizer_email = serializers.CharField(source = "creator.email")
    remaining_tickets = serializers.IntegerField(read_only = True, required = False)
    inpersonevent = InPersonEventSerializer()
    onlineevent = OnlineEventSerializer()
    tags = serializers.SlugRelatedField(many = True, slug_field = "label",
                                        queryset = models.Tag.objects.all())

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
            "organizer_name",
            "organizer_photo",
            "organizer_email",
            "organizer_phone",
            "organizer_SSN",
            "photo",
            "onlineevent",
            "inpersonevent",
            "tags",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if self.context.get("userprofile") is None:
            return representation
        
        enrolled_events = self.context.get("enrolled_events")
        if enrolled_events.filter(id = instance.id).exists():
            representation["enrolled"] = True
        else:
            representation["enrolled"] = False

        bookmarked_events = self.context.get("bookmarked_events")
        if bookmarked_events.filter(id = instance.id).exists():
            representation["bookmarked"] = True
        else:
            representation["bookmarked"] = False
        
        return representation
    