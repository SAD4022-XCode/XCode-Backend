from django.http import HttpRequest
from django.db.models import F
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
        "list": serializers.CommentSerializer,
        "retrieve": serializers.CommentSerializer,
        "create": serializers.CreateCommentSerializer,
        "update": serializers.CreateCommentSerializer,
        "partial_update": serializers.CreateCommentSerializer,
        "reply": serializers.CreateCommentSerializer,
        "like": None,
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
        queryset = self.filter_queryset(self.get_queryset()).filter(parent_id = None)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(operation_summary = "Retrieve a comment")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided"},
                            status = status.HTTP_401_UNAUTHORIZED)
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.user_id != request.user.id:
            return Response({"detail": "operation not allowed, you are not the creator of this comment"},
                            status = status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided"},
                            status = status.HTTP_401_UNAUTHORIZED)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided"},
                            status = status.HTTP_401_UNAUTHORIZED)
        instance = self.get_object()

        if instance.user_id != request.user.id:
            return Response({"detail": "operation not allowed, you are not the creator of this comment"},
                        status = status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
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
    
    @swagger_auto_schema(method = "post", operation_summary = "Like a comment")
    @action(detail = True, methods = ["POST"], permission_classes =  [permissions.IsAuthenticated])
    def like(self, request, pk = None):
        queryset = self.get_queryset()
        queryset.filter(pk = pk).update(score = F("score") + 1)
        return Response(status = status.HTTP_204_NO_CONTENT)
    
