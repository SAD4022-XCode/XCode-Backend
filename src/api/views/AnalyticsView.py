from rest_framework.response import Response
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema

from data import models
from service import serializers

@swagger_auto_schema(method = "GET", responses = {200: serializers.AnalyticsSerializer})
@api_view(http_method_names = ["GET"])
def Analytics(request):
    queryset = models.Event.objects.all()
    
    free_events = queryset.filter(is_paid = False)
    paid_events = queryset.filter(is_paid = True)

    inperson_events = queryset.filter(attendance = 'I')
    online_events = queryset.filter(attendance = 'O')

    registered_users = models.User.objects.all().count()

    response = {
        "registered_users": registered_users,
        "free_inperson_events": (free_events & inperson_events).count(),
        "paid_inperson_events": (paid_events & inperson_events).count(),
        "free_online_events": (free_events & online_events).count(),
        "paid_online_events": (paid_events & online_events).count(),
    }

    serializer = serializers.AnalyticsSerializer(data = response)
    serializer.is_valid(raise_exception = True)

    return Response(serializer.data)