from rest_framework import serializers

class CreateEventSerializer(serializers.Serializer):
    title = serializers.CharField(max_length = 255)
    category = serializers.CharField(max_length = 255)
    description = serializers.CharField()
    starts = serializers.DateTimeField()
    ends = serializers.DateTimeField()
    attendance = serializers.CharField(max_length = 1)
    maximum_tickets = serializers.IntegerField()
    is_paid = serializers.BooleanField()
    ticket_price = serializers.IntegerField(required = False)
    organizer_phone = serializers.CharField(max_length = 11)
    organizer_SSN = serializers.CharField(max_length = 11)
    photo = serializers.ImageField()
    
    url = serializers.URLField(required = False)
    province = serializers.CharField(max_length = 255, required = False)
    city = serializers.CharField(max_length = 255, required = False)
    address = serializers.CharField(max_length = 255, required = False)
    location_lat = serializers.DecimalField(max_digits = 17, decimal_places = 15, required = False)
    location_lon = serializers.DecimalField(max_digits = 18, decimal_places = 15, required = False)

    tags = serializers.ListField(required = False)


    
