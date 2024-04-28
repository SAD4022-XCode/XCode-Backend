from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpRequest
from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema

from data.models import Event, InPersonEvent, OnlineEvent
from service import serializers

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer
    parser_classes = [JSONParser, MultiPartParser]

    serializer_action_classes = {
        "create_event": serializers.CreateEventSerializer,
        "all_events": serializers.EventSerializer,
        "update": serializers.EventInfoSerializer,
        "partial_update": serializers.EventInfoSerializer,
        "retrieve": serializers.EventInfoSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except(KeyError, AttributeError):
            return super().get_serializer_class()
        
    @swagger_auto_schema(operation_summary = "List of all events")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary = "Event details")
    def retrieve(self, request: HttpRequest, *args, **kwargs):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        instance = Event.objects.get(pk = filter_kwargs.get("pk"))

        if instance.attendance == "I":
            obj = InPersonEvent.objects.select_related("event").get(event_id = instance.id)
            event_serializer = self.get_serializer(obj)
            return Response(event_serializer.data)
        
        elif instance.attendance == "O":
            obj = OnlineEvent.objects.select_related("event").get(event_id = instance.id)
            serializer = self.get_serializer(obj)
            return Response(serializer.data)

        return Response(status = status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(method = "post", operation_summary = "Create a new event")
    @action(detail = False, methods = ['POST'], permission_classes = [IsAuthenticated])
    def create_event(self, request: HttpRequest):
        serializer_class = self.get_serializer
        data = request.data
        event_data = {"event": {}}

        for key in data:
            if key in serializers.EventSerializer().get_fields().keys():
                event_data["event"][key] = data[key]                

        if event_data.get("event").get("attendance") == 'I':
            serializer = serializers.InPersonEventSerializer()
            for key in data:
                if (key in serializer.get_fields().keys()):
                    event_data[key] = data[key]
            serializer = serializers.InPersonEventSerializer(data = event_data,
                                                 context = {"user_id": request.user.id})                                   
            serializer.is_valid(raise_exception = True)
            serializer.save()
        
        elif event_data["event"]["attendance"] == 'O':
            serializer = serializers.OnlineEventSerializer()
            for key in data:
                if (key in serializer.get_fields().keys()):
                    event_data[key] = data[key]
            serializer = serializers.OnlineEventSerializer(data = event_data, 
                                               context = {"user_id": request.user.id})
            serializer.is_valid(raise_exception = True)
            serializer.save()
        
        if "tags" in data:
            from data.models import EventTag
            tag_data = data.pop("tags", {})
            for tag in tag_data:
                EventTag.objects.create(tag = tag_data[tag], event_id = serializer.data["event"].get("id"))
        
        return Response(serializer.data) 
        
    @action(detail = False, methods = ["PUT"], permission_classes = [IsAuthenticated])
    def update_event(self, request: HttpRequest):
        if request.data.get("attendance") == 'I':
            serializer = serializers.InPersonEventSerializer(data = request.data,
                                                 partial = True,
                                                 context = {"user_id": request.user.id})
            serializer.is_valid(raise_exception = True)
            event = serializer.save()
            serializer = serializers.InPersonEventSerializer(event)
            return Response(serializer.data)
        
        elif request.data.get("attendance") == 'O':
            serializer = serializers.OnlineEventSerializer(data = request.data,
                                               parial = True,
                                               context = {"user_id": request.user.id})
            serializer.is_valid(raise_exception = True)
            event = serializer.save()
            serializer = serializers.OnlineEventSerializer(event)
            return Response(serializer.data) 

    def destroy(self, request, *args, **kwargs):
        permission_classes = [IsAuthenticated]
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        instance = Event.objects.get(pk = filter_kwargs.get("pk"))
        if instance.creator_id != request.user.id:
            return Response(status = status.HTTP_401_UNAUTHORIZED)
        
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
        

        
