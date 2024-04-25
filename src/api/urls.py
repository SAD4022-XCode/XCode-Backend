from rest_framework import routers
from . import views  

router = routers.DefaultRouter()

router.register("account", views.UserProfileViewSet, basename = "account")
router.register("", views.UserListViewSet, basename = "list")
router.register("event", views.EventViewSet, basename = "event")
urlpatterns = router.urls

