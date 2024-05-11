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
    ticket_price = serializers.DecimalField(max_digits = 6, decimal_places = 2, required = False)
    organizer_phone = serializers.CharField(max_length = 11)
    organizer_SSN = serializers.CharField(max_length = 11)
    photo = serializers.ImageField()
    
    url = serializers.URLField(required = False)
    province = serializers.CharField(max_length = 255, required = False)
    city = serializers.CharField(max_length = 255, required = False)
    address = serializers.CharField(max_length = 255, required = False)
    location_lat = serializers.DecimalField(max_digits = 9, decimal_places = 6, required = False)
    location_lon = serializers.DecimalField(max_digits = 9, decimal_places = 6, required = False)

    tags = serializers.ListField(required = False)


    
