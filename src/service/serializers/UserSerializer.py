from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

class UserSerializer(BaseUserSerializer):
    id = serializers.IntegerField(read_only = True)

    class Meta(BaseUserSerializer.Meta):
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email'
        ]