from rest_framework import serializers

from data import models
from service.serializers.UserSerializer import UserSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many = False)

    class Meta:
        model = models.UserProfile
        fields = [
            'user',
            'gender', 
            'city',
            'birth_date', 
            'profile_picture'
        ]

    def update(self, instance, validated_data):
        user_serializer = self.fields['user']
        user_instance = instance.user
        user_data = validated_data.pop('user', {})

        user_serializer.update(user_instance, user_data)
        return super().update(instance, validated_data)
