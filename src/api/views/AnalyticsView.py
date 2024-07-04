from rest_framework.response import Response
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema

from data import models
from service import serializers

@swagger_auto_schema(method = "GET", responses = {200: serializers.AnalyticsSerializer})
@api_view(http_method_names = ["GET"])
def Analytics(request):
    queryset = models.Event.objects.all()
    
    free_events = queryset.filter(is_paid = False).count()
    paid_events = queryset.filter(is_paid = True).count()

    in_person_events = queryset.filter(attendance = 'I').count()
    online_events = queryset.filter(attendance = 'O').count()

    response = {
        "free_events": free_events,
        "paid_events": paid_events,
        "in_person_events": in_person_events,
        "online_events": online_events,
    }

    serializer = serializers.AnalyticsSerializer(data = response)
    serializer.is_valid(raise_exception = True)

    return Response(serializer.data)