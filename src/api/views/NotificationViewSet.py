from rest_framework import viewsets
from rest_framework import parsers
from rest_framework import mixins
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from data import models
from service import serializers

class NotificationViewSet(mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    
    queryset = models.Notification.objects \
        .select_related("recipient").all()
    
    serializer_class = serializers.NotificationSerializer
    parser_classes = [
        parsers.JSONParser,
        parsers.MultiPartParser,
    ]

    serializer_action_classes = {
        "list": serializer_class,
        "mark_as_read": None,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except(KeyError, AttributeError):
            return super().get_serializer_class()

    @swagger_auto_schema(operation_summary = "List of all notifications")
    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided"},
                            status = status.HTTP_401_UNAUTHORIZED)

        # queryset = self.get_queryset().filter(recipient_id = request.user.id)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many = True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data)
    
    @swagger_auto_schema(operation_summary = "Delete a notification (login required)")
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided"},
                            status = status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()

        if instance.recipient_id != request.user.id:
            return Response({"detail": "operation not allowed, you are not the recipient of this notification"}, 
                            status = status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(method = "patch", operation_summary = "Mark notification as read (login required)")
    @action(detail = True, methods = ["PATCH"], permission_classes = [permissions.IsAuthenticated])
    def mark_as_read(self, request, pk = None):
        instance = self.get_object()

        if instance.recipient_id != request.user.id:
            return Response({"detail": "operation not allowed, you are not the recipient of this notification"}, 
                            status = status.HTTP_403_FORBIDDEN)
        
        if instance.is_read == True:
            return Response(status = status.HTTP_204_NO_CONTENT)
        instance.is_read = True;        
        instance.save(update_fields = ["is_read"])

        return Response(status = status.HTTP_204_NO_CONTENT)
