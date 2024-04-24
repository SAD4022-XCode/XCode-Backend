from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpRequest, FileResponse
from rest_framework.permissions import IsAuthenticated

from data.models import Event
from service.serializers import EventSerializer, InPersonEventSerializer, OnlineEventSerializer

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @action(methods = ['POST'], permission_classes = [IsAuthenticated])
    def create(self, request: HttpRequest):
        if request.data.get("attendance") == 'I':
            serializer = InPersonEventSerializer(data = request.data,
                                                 context = {"user_id": request.user.id})
            serializer.is_valid(raise_exception = True)
            event = serializer.save()
            serializer = InPersonEventSerializer(event)
            return Response(serializer.data)
        
        elif request.data.get("attendance") == 'O':
            serializer = OnlineEventSerializer(data = request.data,
                                               context = {"user_id": request.user.id})
            serializer.is_valid(raise_exception = True)
            event = serializer.save()
            serializer = OnlineEventSerializer(event)
            return Response(serializer.data) 
        
    @action(methods = ["PUT"], permission_classes = [IsAuthenticated])
    def update(self, request: HttpRequest):
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
    
    @action(methods = ['DELETE'], permission_classes = [IsAuthenticated])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
        

        
