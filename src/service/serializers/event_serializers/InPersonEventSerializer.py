from rest_framework import serializers

from data import models

class InPersonEventSerializer(serializers.ModelSerializer):
    # event = EventSerializer(partial = True)

    class Meta:
        model = models.InPersonEvent
        fields = [
            # "event",
            "province",
            "city",
            "address",
            "location_lat",
            "location_lon",
        ]

    def create(self, validated_data):
        in_person_event = models.InPersonEvent.objects.create(event_id = self.context.get("event_id"), 
                                                              **validated_data)  

        return in_person_event