from rest_framework import serializers

from data import models
from service.serializers.MyUserSerializer import MyUserSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    user = MyUserSerializer(many = False, partial = True)

    class Meta:
        model = models.UserProfile
        fields = [
            'user',
            'gender', 
            'city',
            'province',
            'birth_date', 
            'profile_picture'
        ]

    def update(self, instance, validated_data):
        user_serializer = self.fields['user']
        user_instance = instance.user
        user_data = validated_data.pop('user', {})
        user_serializer.update(user_instance, user_data)

        if ('profile_picture' in validated_data):
            instance.profile_picture.delete(save = True)

        return super().update(instance, validated_data)
