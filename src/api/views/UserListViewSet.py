from django.http import HttpRequest
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser

from data.models import UserProfile
from service.serializers import UserProfileSerializer

class UserListViewSet(ModelViewSet):
    queryset = UserProfile.objects.select_related('user').all()
    permission_classes = [AllowAny]
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=False, methods=['GET'], permission_classes = [AllowAny])
    def user_list(self, request: HttpRequest):
        users = UserProfile.objects.select_related('user').all()

        if (request.method == 'GET'):
            serializer = UserProfileSerializer(users, many = True)
            return Response(serializer.data) 
