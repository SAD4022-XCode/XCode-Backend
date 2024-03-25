from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from service.serializers.UserProfileSerializer import UserProfileSerializer

class UserSerializer(BaseUserSerializer):

    # gender = serializers.CharField(source = 'userprofile.gender', required = False)
    # birth_date = serializers.DateField(source = 'userprofile.birth_date', required = False)
    # city = serializers.CharField(source = 'userprofile.city', required = False)
    # profile_picture = serializers.ImageField(source = 'userprofile.profile_picture', required = False)

    class Meta(BaseUserSerializer.Meta):
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email'
            # 'birth_date',
            # 'gender',
            # 'city',
            # 'profile_picture'
        ]