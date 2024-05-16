from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.http import HttpRequest
from django.db import transaction
from django.db.models import Q
from django_filters import rest_framework as filters
from django import shortcuts
from datetime import datetime, timezone
import json

from drf_yasg.utils import swagger_auto_schema

from data import models
from service.serializers import event_serializers
from service import serializers
from service import pagination
from service.filters import EventFilter

class EventViewSet(ModelViewSet):
    queryset = models.Event.objects \
        .select_related("inpersonevent", "onlineevent", "creator") \
        .prefetch_related("tags") \
        .all()
    serializer_class = event_serializers.EventSerializer
    parser_classes = [JSONParser, MultiPartParser]
    pagination_class = pagination.CustomPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EventFilter

    serializer_action_classes = {
        "create": event_serializers.CreateEventSerializer,
        "list": event_serializers.EventSummarySerializer,
        "update": event_serializers.EventDetailSerializer,
        "partial_update": event_serializers.EventDetailSerializer,
        "retrieve": event_serializers.EventDetailSerializer,
        "leave_comment": serializers.CreateCommentSerializer,
        "comments": serializers.CommentListSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except(KeyError, AttributeError):
            return super().get_serializer_class()

    @swagger_auto_schema(operation_summary = "List of all events")
    def list(self, request, *args, **kwargs):
        start = request.GET.get("starts")
        end = request.GET.get("ends")
        date_filter = EventFilter({"starts_after": start, "ends_before": end})
        filtered_queryset = date_filter.qs

        filter = EventFilter(request.GET, queryset = filtered_queryset)
        filtered_queryset = filter.qs
        
        if (request.GET.get("tags") is not None):
            tag_list = request.GET.get("tags").strip().split(', ')

            tags = models.Tag.objects.filter(label__in = tag_list)
            filtered_queryset = filtered_queryset.filter(tags__in = tags).distinct()

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary = "Create a new event")
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided"},
                            status = status.HTTP_401_UNAUTHORIZED)

        data = request.data
        tags = json.loads(data.get("tags"))
        event_serializer = event_serializers.EventSerializer(data = data, 
                                                             context = {
                                                                 "user_id": request.user.id,
                                                                 "tags": tags,
                                                                        })
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
        
        return Response(event_serializer.data.get("id")) 

    @swagger_auto_schema(operation_summary = "Event details")
    @transaction.atomic
    def retrieve(self, request: HttpRequest, *args, **kwargs):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        queryset = self.get_queryset()
        instance = shortcuts.get_object_or_404(queryset, pk = filter_kwargs.get("pk"))

        serializer = self.get_serializer(instance)
        return Response(serializer.data)            
    
    @swagger_auto_schema(operation_summary = "Update event")
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided"},
                            status = status.HTTP_401_UNAUTHORIZED)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.creator_id != request.user.id:
            return Response({"detail": "operation not allowed, you are not the creator of this event"},
                            status = status.HTTP_403_FORBIDDEN)
        
        if datetime.now(tz = timezone.utc) > instance.starts:
            return Response({"detail": "operation not allowed, the event has started"}, 
                            status = status.HTTP_403_FORBIDDEN)

        tags = request.data.get("tags")
        for tag in tags:
            models.Tag.objects.get_or_create(label = tag)

        serializer = self.get_serializer(instance, data = request.data, partial = partial)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    @swagger_auto_schema(operation_summary = "Partial-update event")
    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided"},
                            status = status.HTTP_401_UNAUTHORIZED)

        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
            
    @swagger_auto_schema(operation_summary = "Delete an event")
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided"},
                            status = status.HTTP_401_UNAUTHORIZED)
        
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        queryset = self.get_queryset()

        instance = shortcuts.get_object_or_404(queryset, pk = filter_kwargs.get("pk"))

        if instance.creator_id != request.user.id:
            return Response({"detail": "operation not allowed, you are not the creator of this event"}, 
                            status = status.HTTP_403_FORBIDDEN)
        
        if datetime.now(tz = timezone.utc) > instance.starts:
            return Response({"detail": "operation not allowed, the event has started"}, 
                            status = status.HTTP_403_FORBIDDEN)

        instance.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(operation_summary = "List of comments under event")
    @action(detail = True, methods = ["GET"])
    def comments(self, request, pk = None):
        queryset = models.Comment.objects \
            .prefetch_related("children", "liked_by") \
            .select_related("user", "user__userprofile", "event") \
            .filter(Q(event_id = pk) & Q(parent_id = None))
    
        serializer = self.get_serializer(queryset, 
                                         many = True,
                                         context = {
                                             "request_user": request.user.id,
                                             "request": request,
                                                    })
        return Response({"comments": serializer.data})    
        

        
