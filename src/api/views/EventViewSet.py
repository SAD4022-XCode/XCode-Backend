from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.db import transaction
from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema

from data.models import Event
from service.serializers import event_serializers
from service import serializers

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = event_serializers.EventSerializer
    parser_classes = [JSONParser, MultiPartParser]

    serializer_action_classes = {
        "create_event": event_serializers.CreateEventSerializer,
        "list": event_serializers.EventSummarySerializer,
        "update": event_serializers.EventDetailSerializer,
        "partial_update": event_serializers.EventDetailSerializer,
        "retrieve": event_serializers.EventDetailSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except(KeyError, AttributeError):
            return super().get_serializer_class()
        
    @swagger_auto_schema(operation_summary = "List of all events")
    def list(self, request, *args, **kwargs):
        queryset = Event.objects.select_related("inpersonevent", "onlineevent")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary = "Event details")
    @transaction.atomic
    def retrieve(self, request: HttpRequest, *args, **kwargs):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        
        try:
            instance = Event.objects \
                .select_related("inpersonevent", "onlineevent") \
                .get(pk = filter_kwargs.get("pk"))
        
        except Event.objects.model.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @swagger_auto_schema(method = "post", operation_summary = "Create a new event")
    @transaction.atomic
    @action(detail = False, methods = ['POST'], permission_classes = [IsAuthenticated])
    def create_event(self, request: HttpRequest):
        data = request.data

        event_serializer = event_serializers.EventSerializer(data = data, 
                                                             context = {"user_id": request.user.id})
        event_serializer.is_valid(raise_exception = True)
        event_serializer.save()
        event_id = event_serializer.data.get("id")

        if data.get("attendance") == 'I':
            serializer = event_serializers.InPersonEventSerializer(data = data,
                                                 context = {"event_id": event_id})                                   
            serializer.is_valid(raise_exception = True)
            serializer.save()
        
        elif data.get("attendance") == 'O':
            serializer = event_serializers.OnlineEventSerializer(data = data, 
                                               context = {"event_id": event_id})
            serializer.is_valid(raise_exception = True)
            serializer.save()
        
        if "tags" in data:
            from data.models import EventTag
            tag_data = data.pop("tags", {})
            for tag in tag_data:
                tag_serializer = serializers.EventTagSerializer(data = {"tag": tag},
                                                                context = {"event_id": event_id})      
                tag_serializer.is_valid(raise_exception = True)
                tag_serializer.save()
                    
        return Response(serializer.data) 
        
    @action(detail = False, methods = ["PUT"], permission_classes = [IsAuthenticated])
    @transaction.atomic
    def update_event(self, request: HttpRequest):
        if request.data.get("attendance") == 'I':
            serializer = event_serializers.InPersonEventSerializer(data = request.data,
                                                 partial = True,
                                                 context = {"user_id": request.user.id})
            serializer.is_valid(raise_exception = True)
            event = serializer.save()
            serializer = event_serializers.InPersonEventSerializer(event)
            return Response(serializer.data)
        
        elif request.data.get("attendance") == 'O':
            serializer = event_serializers.OnlineEventSerializer(data = request.data,
                                               parial = True,
                                               context = {"user_id": request.user.id})
            serializer.is_valid(raise_exception = True)
            event = serializer.save()
            serializer = event_serializers.OnlineEventSerializer(event)
            return Response(serializer.data) 

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        permission_classes = [IsAuthenticated]
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        try:
            instance = Event.objects.get(pk = filter_kwargs.get("pk"))

        except Event.objects.model.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        if instance.creator_id != request.user.id:
            return Response(status = status.HTTP_401_UNAUTHORIZED)
        
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
        

        
