from django_filters import rest_framework

from data import models

class EventFilter(rest_framework.FilterSet):
    starts = rest_framework.IsoDateTimeFromToRangeFilter()
    ends = rest_framework.IsoDateTimeFromToRangeFilter()
    eventtag = rest_framework.AllValuesFilter()

    class Meta:
        model = models.Event
        fields = [
            "attendance",
            "is_paid",
            "starts",
            "ends",
            "eventtag",
        ]
