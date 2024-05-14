from django.http import HttpRequest
from rest_framework import viewsets
from rest_framework import parsers
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema

from data import models
from service import serializers
from service import pagination

class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.prefetch_related("children").all()
    serializer_class = serializers.CommentSerializer
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]
    pagination_class = pagination.CustomPagination

    serializer_action_classes = {
        "create" : serializers.CreateCommentSerializer,
        "reply" : serializers.CreateCommentSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except(KeyError, AttributeError):
            return super().get_serializer_class()

    @swagger_auto_schema(operation_summary = "Leave a comment")
    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided"},
                            status = status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.get_serializer(data = request.data, 
                                         context = {
                                            "user_id": request.user.id,
                                         })
        serializer.is_valid(raise_exception = True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status = status.HTTP_201_CREATED, headers = headers)

    @swagger_auto_schema(operation_summary = "List of all comments")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary = "Retrieve a comment")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(method = "post", operation_summary = "Reply on a comment")
    @action(detail = True, methods = ["POST"], permission_classes = [permissions.IsAuthenticated])
    def reply(self, request: HttpRequest, pk = None):
        request.data
        serializer = self.get_serializer(data = request.data,
                                         context = {
                                             "parent_id" : pk,
                                             "user_id": request.user.id
                                         })
        serializer.is_valid(raise_exception = True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status = status.HTTP_201_CREATED, headers = headers)
    
