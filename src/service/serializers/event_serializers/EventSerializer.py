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

    def create(self, validated_data):
        instance = models.Event.objects.create(creator_id = self.context.get("user_id"), **validated_data)
        return instance
        
