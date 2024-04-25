from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpRequest, FileResponse

from data.models import Event
from service.serializers import EventSerializer, CreateEventSerializer, InPersonEventSerializer, OnlineEventSerializer

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    @action(detail = False, methods = ['GET'])
    def all_events(self, request, *args, **kwargs):
        serializer = EventSerializer(self.queryset, many = True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        data = request.data
        event = self.queryset.get(id = data.get("id"))
    
    @action(detail = False, methods = ['POST'], permission_classes = [IsAuthenticated])
    def create_event(self, request: HttpRequest):
        event_data = request.data

        if event_data["event"].get("attendance") == 'I':
            serializer = InPersonEventSerializer(data = event_data,
                                                 context = {"user_id": request.user.id})                                   
            serializer.is_valid(raise_exception = True)
            # serializer.save()
            return Response(serializer.data)
        
        elif event_data["event"].get("attendance") == 'O':
            serializer = OnlineEventSerializer(data = event_data,
                                               context = {"user_id": request.user.id})
            serializer.is_valid(raise_exception = True)
            # serializer.save()
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
        

        
