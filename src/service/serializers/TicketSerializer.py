from rest_framework import serializers

from data import models

class TicketSerializer(serializers.ModelSerializer):
    attendee = serializers.PrimaryKeyRelatedField(queryset = models.UserProfile.objects \
                                                  .prefetch_related("enrolled_events") \
                                                  .all(),
                                                  required = False)
    event = serializers.PrimaryKeyRelatedField(queryset = models.Event.objects.all(), 
                                               required = False)


    class Meta:
        model = models.Ticket
        fields = [
            "attendee",
            "attendee_name",
            "attendee_email",
            "attendee_phone",
            "price",
            "event",
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def save(self, **kwargs):
        return super().save(**kwargs)