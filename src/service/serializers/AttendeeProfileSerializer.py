from rest_framework import serializers
from data import models

class AttendeeProfileSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only = True)

    class Meta:
        model = models.AttendeeProfile
        fields = ['id', 'user_id', 'birth_date']