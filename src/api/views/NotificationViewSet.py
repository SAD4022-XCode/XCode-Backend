from rest_framework import viewsets
from rest_framework import parsers
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status

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

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided"},
                            status = status.HTTP_401_UNAUTHORIZED)

        queryset = self.get_queryset().filter(recipient_id = request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many = True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data)
    
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
