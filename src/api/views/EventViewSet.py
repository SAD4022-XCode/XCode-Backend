from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpRequest

from data.models import Event, InPersonEvent, OnlineEvent
from service.serializers import EventSerializer, CreateEventSerializer, EventInfoSerializer, InPersonEventSerializer, OnlineEventSerializer

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    parser_classes = [JSONParser, MultiPartParser]

    serializer_action_classes = {
        "create_event": CreateEventSerializer,
        "all_events": EventSerializer,
        "update": EventInfoSerializer,
        "partial_update": EventInfoSerializer,
        "retrieve": EventInfoSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except(KeyError, AttributeError):
            return super().get_serializer_class()

    @action(detail = False, methods = ['GET'])
    def all_events(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many = True)
        return Response(serializer.data)

    # @action(detail = False, methods = ['POST'])
    def retrieve(self, request: HttpRequest, *args, **kwargs):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        lookup = filter_kwargs.get("pk")

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
    
    @action(detail = False, methods = ['POST'], permission_classes = [IsAuthenticated])
    def create_event(self, request: HttpRequest):
        serializer_class = self.get_serializer
        data = request.data
        event_data = {"event": {}}

        for key in data:
            if key in EventSerializer().get_fields().keys():
                event_data["event"][key] = data[key]

        if event_data["event"]["attendance"] == 'I':
            serializer = InPersonEventSerializer()
            for key in data:
                if (key in serializer.get_fields().keys()):
                    event_data[key] = data[key]
            serializer = InPersonEventSerializer(data = event_data,
                                                 context = {"user_id": request.user.id})                                   
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(serializer.data)
        
        elif event_data["event"]["attendance"] == 'O':
            serializer = OnlineEventSerializer()
            for key in data:
                if (key in serializer.get_fields().keys()):
                    event_data[key] = data[key]
            serializer = OnlineEventSerializer(data = event_data, 
                                               context = {"user_id": request.user.id})
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(serializer.data) 
        
    @action(detail = False, methods = ["PUT"], permission_classes = [IsAuthenticated])
    def update_event(self, request: HttpRequest):
        if request.data.get("attendance") == 'I':
            serializer = InPersonEventSerializer(data = request.data,
                                                 partial = True,
                                                 context = {"user_id": request.user.id})
            serializer.is_valid(raise_exception = True)
            event = serializer.save()
            serializer = InPersonEventSerializer(event)
            return Response(serializer.data)
        
        elif request.data.get("attendance") == 'O':
            serializer = OnlineEventSerializer(data = request.data,
                                               parial = True,
                                               context = {"user_id": request.user.id})
            serializer.is_valid(raise_exception = True)
            event = serializer.save()
            serializer = OnlineEventSerializer(event)
            return Response(serializer.data) 
    
    @action(detail = False, methods = ['DELETE'], permission_classes = [IsAuthenticated])
    def delete_event(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
        

        
