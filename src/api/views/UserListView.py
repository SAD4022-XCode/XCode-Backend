from rest_framework.response import Response
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema

from data.models import UserProfile
from service.serializers import UserProfileSerializer

@swagger_auto_schema(method = "get", operation_summary = "List of all registered users")
@api_view()
def UserList(request):
    users = UserProfile.objects.select_related("user").all()
    serializer = UserProfileSerializer(users, many = True)
    return Response(serializer.data)