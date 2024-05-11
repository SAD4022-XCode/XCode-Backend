from rest_framework import serializers

from data import models

class EventSummarySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length = 255)
    category = serializers.CharField(max_length = 255)
    attendance = serializers.CharField(max_length = 1)
    is_paid = serializers.BooleanField()
    ticket_price = serializers.IntegerField(required = False)
    start_date = serializers.DateField()
    photo = serializers.ImageField()
    province = serializers.CharField(max_length = 255, source = "inpersonevent.province")
    city = serializers.CharField(max_length = 255, source = "inpersonevent.city")
    tags = serializers.SlugRelatedField(many = True, slug_field = "label", 
                                        queryset = models.Tag.objects.all())

    class Meta:
        model = models.Event
        fields = [
            "id",
            "title",
            "category",
            "attendance",
            "is_paid",
            "ticket_price",
            "start_date",
            "photo",
            "province",
            "city",
            "tags",
        ]
