from rest_framework import serializers

from data import models

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username')
    firstname = serializers.CharField(source = 'user.first_name')
    lastname = serializers.CharField(source = 'user.last_name')
    email = serializers.EmailField(source = 'user.email')
    profile_picture = serializers.ImageField(required = False)

    # Implement custom update() method for updating user(relation) data

    class Meta:
        model = models.UserProfile
        fields = [
            'firstname', 
            'lastname', 
            'username', 
            'email', 
            'gender', 
            'city',
            'birth_date', 
            'profile_picture'
        ]