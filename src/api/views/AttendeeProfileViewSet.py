from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from data.models import AttendeeProfile
from service.serializers import AttendeeProfileSerializer

class AttendeeProfileViewSet(ModelViewSet):
    queryset = AttendeeProfile.objects.all()
    serializer_class = AttendeeProfileSerializer
    permission_classes = [permissions.IsAdminUser]


    @action(detail = False, methods = ['GET', 'PUT'], permission_classes = [permissions.IsAuthenticated])
    def me(self, request):
        (attendee, created) = AttendeeProfile.objects.get_or_create(user_id = request.user.id)
        if request.method == 'GET':
            serializer = AttendeeProfileSerializer(attendee)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = AttendeeProfileSerializer(attendee, data = request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(serializer.data)