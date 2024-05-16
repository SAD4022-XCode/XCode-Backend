from rest_framework import viewsets
from rest_framework import parsers

from data import models
from service import serializers

class RatingViewSet(viewsets.ModelViewSet):
    queryset = models.Rating.objects \
        .select_related("event", "user") \
        .all()
    
    serializer_class = serializers.RatingSerializer
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)