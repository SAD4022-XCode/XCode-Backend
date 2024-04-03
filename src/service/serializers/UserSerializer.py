from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from data.models import User

class UserSerializer(BaseUserSerializer):
    id = serializers.IntegerField(read_only = True)
    first_name = serializers.CharField(read_only = True)
    last_name = serializers.CharField(read_only = True)
    email = serializers.CharField(read_only = True)
    username = serializers.CharField(read_only = False)

    class Meta(BaseUserSerializer.Meta):
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email'
        ]

    def update(self, instance, validated_data):
        if ('username' in validated_data):
            new_username = validated_data['username']
            setattr(instance, User.USERNAME_FIELD, new_username)
            instance.save()

        return super().update(instance, validated_data)