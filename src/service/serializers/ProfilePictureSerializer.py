from rest_framework import serializers
from data import models

class ProfilePictureSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField()

    class Meta:
        model = models.UserProfile
        fields = ['profile_picture']

    def update(self, instance, validated_data):
        if ('profile_picture' in validated_data):
            instance.profile_picture.delete(save = True)
            
        return super().update(instance, validated_data)

