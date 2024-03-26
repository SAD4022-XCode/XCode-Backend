from django.http import HttpRequest
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from data.models import UserProfile
from service import serializers

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    #Implement PATCH

    @action(detail = False, methods = ['GET', 'PUT', 'PATCH'], permission_classes = [permissions.IsAuthenticated])
    def me(self, request: HttpRequest):
        profile = UserProfile.objects.get(user_id = request.user.id)

        if request.method == 'GET':
            serializer = serializers.UserProfileSerializer(profile)
            return Response(serializer.data)
                    
        elif request.method == 'PUT':
            serializer = serializers.UserProfileSerializer(profile, data = request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()

            return Response(serializer.data)
        
        elif request.method == 'PATCH':
            serializer = serializers.UserProfileSerializer(profile, 
                                                           data = request.data, 
                                                           partial = True)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(serializer.data)
            # self.partial_update(request)

    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)

    