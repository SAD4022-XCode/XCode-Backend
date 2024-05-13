from api.views.UserProfileViewSet import UserProfileViewSet
from api.views.EventViewSet import EventViewSet, EventDetails
from api.views.SwaggerSchemaView import SwaggerSchemaView
from api.views.CommentViewSet import CommentViewSet
from api.views.UserListView import UserList

__all__ = [
    UserProfileViewSet,
    EventViewSet,
    SwaggerSchemaView,
    EventDetails,
    CommentViewSet,
    UserList,
]
