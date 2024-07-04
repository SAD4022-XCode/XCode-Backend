from django.urls import path
from rest_framework import routers
from . import views  

urlpatterns = [
    path("all_users/", views.UserList, name = "all"),
    path("analytics/", views.Analytics, name = "analytics"),
]

router = routers.DefaultRouter()

router.register("account", views.UserProfileViewSet, basename = "account")
router.register("events", views.EventViewSet, basename = "events")
router.register("comments", views.CommentViewSet, basename = "comments")
router.register("notifications", views.NotificationViewSet, basename = "notifications")
router.register("conversations", views.ConversationViewSet, basename = "conversations")
router.register("messages", views.MessageViewSet, basename = "messages")

urlpatterns += router.urls

