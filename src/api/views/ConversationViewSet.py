from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import parsers
from rest_framework import decorators
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.db import transaction

from data import models
from service import serializers
class ConversationViewSet(viewsets.GenericViewSet):
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
    
    @decorators.action(detail = True, methods = ["GET"], permission_classes = [permissions.IsAuthenticated])
    @transaction.atomic
    def message_history(self, request, pk = None):
        if not models.UserConversation.objects \
            .filter(Q(user_id = request.user.id) & Q(conversation_id = pk)) \
            .exists():
            return Response({"detail": "Forbidden"}, status = status.HTTP_403_FORBIDDEN)
        conversation = self.get_object()
        messages = conversation.message_history
        serializer = serializers.MessageSerializer(messages, 
                                                   many = True,
                                                   context = {
                                                       "request": request,
                                                   })
        return Response(serializer.data)