from django.http import HttpRequest, FileResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from data.models import UserProfile
from service import serializers

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    serializer_action_classes = {
        'me' : serializers.UserProfileSerializer,
        'get_profile_picture': serializers.ProfilePictureSerializer,
        'set_profile_picture': serializers.ProfilePictureSerializer
    }

    #Implement PATCH

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except(KeyError, AttributeError):
            return super.get_serializer_class()

    @action(detail = False, methods = ['GET', 'PUT', 'PATCH'], permission_classes = [permissions.IsAuthenticated])
    def me(self, request: HttpRequest):
        profile = UserProfile.objects.get_by_id(request.user.id)

        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
                    
        elif request.method == 'PUT':
            serializer = self.get_serializer(profile, data = request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()

            return Response(serializer.data)
        
        elif request.method == 'PATCH':
            serializer = self.get_serializer(profile, data = request.data, partial = True)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(serializer.data)

    @action(detail = False, methods = ['GET'], permission_classes = [permissions.IsAuthenticated])
    def get_profile_picture(self, request: HttpRequest):
        profile = UserProfile.objects.get_by_id(request.user.id)

        if (not profile.profile_picture):
            return Response('User has no profile photos.', status.HTTP_404_NOT_FOUND)
        try:
            return FileResponse(profile.get_profile_picture())
        except(FileNotFoundError):
            return Response('File not found', status = status.HTTP_404_NOT_FOUND)

        
    @action(detail = False, methods = ['PUT', 'DELETE'], permission_classes = [permissions.IsAuthenticated])
    def set_profile_picture(self, request):            
        profile = UserProfile.objects.get_by_id(request.user.id)

        if (request.method == 'PUT'):
            serializer = self.get_serializer(profile, data = request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()

            return Response(f'Image was saved to {profile.profile_picture.url}')
        
        if (request.method == 'DELETE'):
            profile.delete_profile_picture()
            return Response('Profile photo was deleted.', status = status.HTTP_204_NO_CONTENT)