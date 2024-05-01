from rest_framework import serializers

from data import models

class EventSummarySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length = 255)
    category = serializers.CharField(max_length = 255)
    attendance = serializers.CharField(max_length = 1)
    photo = serializers.ImageField()
    province = serializers.CharField(max_length = 255, source = "inpersonevent.province")
    city = serializers.CharField(max_length = 255, source = "inpersonevent.city")

    class Meta:
        model = models.Event
        fields = [
            "id",
            "title",
            "category",
            "attendance",
            "photo",
            "province",
            "city",
        ]
