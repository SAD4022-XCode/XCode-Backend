from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser

from data.models import UserProfile
from service.serializers import UserProfileSerializer

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    #Implement PATCH

    @action(detail = False, methods = ['GET', 'PUT'], permission_classes = [permissions.IsAuthenticated])
    def me(self, request):
        profile = UserProfile.objects.get(user_id = request.user.id)

        if request.method == 'GET':
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(profile, data = request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)