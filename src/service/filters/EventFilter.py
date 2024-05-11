from django_filters import rest_framework
from django import forms

from data import models

class EventFilter(rest_framework.FilterSet):
    starts = rest_framework.IsoDateTimeFromToRangeFilter()
    ends = rest_framework.IsoDateTimeFromToRangeFilter()
    tags = rest_framework.filters.ModelMultipleChoiceFilter(queryset = models.Tag.objects.all(), )

    class Meta:
        model = models.Event
        fields = [
            "attendance",
            "is_paid",
            "starts",
            "ends",
            "tags",
        ]
