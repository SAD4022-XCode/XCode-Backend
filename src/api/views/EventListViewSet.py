from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.db.models import Q
from django_filters import rest_framework as filters

from data import models
from service.serializers.event_serializers import EventSummarySerializer
from service import pagination

from drf_yasg.utils import swagger_auto_schema

class EventFilter(filters.FilterSet):
    starts = filters.IsoDateTimeFromToRangeFilter()
    ends = filters.IsoDateTimeFromToRangeFilter()

    class Meta:
        model = models.Event
        fields = [
            "attendance",
            "is_paid",
            "starts",
            "ends",
        ]

class EventListView(ListAPIView):
    queryset = models.Event.objects.all()
    serializer_class = EventSummarySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EventFilter
    pagination_class = pagination.CustomPagination

    @swagger_auto_schema(operation_summary = "Event Filter")
    def get(self, request, *args, **kwargs):
        start = request.GET.get("starts")
        end = request.GET.get("ends")
        filter1 = EventFilter({"starts_after": start, "ends_before": end})
        filtered_queryset1 = filter1.qs
        filter2 = EventFilter(request.GET, queryset = filtered_queryset1)
        filtered_queryset2 = filter2.qs


        page = self.paginate_queryset(filtered_queryset2)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_queryset2, many = True)
        return Response(serializer.data)