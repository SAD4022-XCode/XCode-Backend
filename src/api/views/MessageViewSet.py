from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import parsers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from django.db import transaction

from data import models
from service import serializers

class MessageViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    queryset = models.Message.objects.prefetch_related("sender", "conversation").all()
    serializer_class = serializers.MessageSerializer
    parser_classes = [
        parsers.JSONParser,
        parsers.MultiPartParser,
    ]

    serializer_action_classes = {
        "create": serializers.MessageCreateSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except(KeyError, AttributeError):
            return super().get_serializer_class()

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs):
        data = request.data.copy()
        sender = models.User.objects.prefetch_related("conversations").get(pk = data.get("sender"))
        recipient = models.User.objects.prefetch_related("conversations").get(pk = data.get("recipient"))

        sender_conversations = sender.conversations.all()
        recipient_conversations = recipient.conversations.all()

        if not (sender_conversations & recipient_conversations).exists():
            # create conversation
            conversation = models.Conversation.objects.create()
            conversation.save()

            sender.conversations.add(conversation)
            recipient.conversations.add(conversation)
        
        else:
            conversation = (sender_conversations & recipient_conversations).first()

        data.update({
            "conversation": conversation.id,
        })
        print(conversation.id)
        print(data)

        serializer = self.get_serializer(data = data)
        print(serializer)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
