from django.urls import path
from rest_framework import routers
from . import views  

urlpatterns = [
    path("all_users/", views.UserList, name = "all"),
]

router = routers.DefaultRouter()

router.register("account", views.UserProfileViewSet, basename = "account")
router.register("events", views.EventViewSet, basename = "events")
router.register("comments", views.CommentViewSet, basename = "comments")
router.register("notifications", views.NotificationViewSet, basename = "notifications")

urlpatterns += router.urls

