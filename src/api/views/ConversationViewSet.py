from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import parsers
from rest_framework import decorators
from rest_framework import permissions
from rest_framework.response import Response
from django.db import transaction

from data import models
from service import serializers
class ConversationViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = models.Conversation.objects \
        .prefetch_related("participants", "message_history") \
        .all()
    serializer_class = serializers.ConversationSerializer
    parser_classes = [
        parsers.MultiPartParser,
        parsers.JSONParser,
    ]

    serializer_action_classes = {
        "list": serializers.ConversationSerializer,
        "message_history": serializers.MessageSerializer,
        "add_message": serializers.MessageSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except(KeyError, AttributeError):
            return super().get_serializer_class()

    @transaction.atomic
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @decorators.action(detail = True, methods = ["GET"], permission_classes = [permissions.IsAuthenticated])
    @transaction.atomic
    def message_history(self, request, pk = None):
        conversation = self.get_object()
        messages = conversation.message_history
        serializer = serializers.MessageSerializer(messages, 
                                                   many = True,
                                                   context = {
                                                       "request": request,
                                                   })
        return Response(serializer.data)