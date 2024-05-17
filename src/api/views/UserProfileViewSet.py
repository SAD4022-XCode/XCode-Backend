from django.http import HttpRequest, FileResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from drf_yasg.utils import swagger_auto_schema

from data.models import UserProfile, Event
from service import serializers
from service.serializers import event_serializers

class UserProfileViewSet(GenericViewSet):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    serializer_action_classes = {
        'me' : serializers.UserProfileSerializer,
        'get_profile_picture': serializers.ProfilePictureSerializer,
        'set_profile_picture': serializers.ProfilePictureSerializer,
        'register_event' : serializers.RegisterEventSerializer,
    }


    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except(KeyError, AttributeError):
            return super().get_serializer_class()
    
    @swagger_auto_schema(method = "get", operation_summary = "Display user info")
    @swagger_auto_schema(method = "put", operation_summary = "Update user info")
    @swagger_auto_schema(method = "patch", operation_summary = "Update User Info")
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
        
    @swagger_auto_schema(operation_summary = "Get user profile photo")
    @action(detail = False, methods = ['GET'], permission_classes = [permissions.IsAuthenticated])
    def get_profile_picture(self, request: HttpRequest):
        profile = UserProfile.objects.get_by_id(request.user.id)

        if (not profile.profile_picture):
            return Response('User has no profile photos.', status.HTTP_404_NOT_FOUND)
        try:
            return FileResponse(profile.get_profile_picture())
        except(FileNotFoundError):
            return Response('File not found', status = status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(method = "put", operation_summary = "Update user profile photo")
    @swagger_auto_schema(method = "delete", operation_summary = "Delete user profile photo")
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

    @swagger_auto_schema(operation_summary = "List of events created by user")
    @action(detail = False, methods = ['GET'], permission_classes = [permissions.IsAuthenticated])    
    def my_events(self, request):
        events = Event.objects.filter(creator_id = request.user.id)
        serializer = event_serializers.EventSummarySerializer(events, many = True)

        return Response(serializer.data)
        
    @swagger_auto_schema(operation_summary = "Save user's registeration")
    @action(detail = False, methods = ['PATCH'], permission_classes = [permissions.IsAuthenticated])
    def register_event(self, request):
        instance = UserProfile.objects.select_related("user").get(user_id = request.user.id)
        if instance is None:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        