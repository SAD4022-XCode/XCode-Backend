from rest_framework import routers
from .views import *  

router = routers.DefaultRouter()

router.register('auth', UserProfileViewSet, basename = 'auth')
router.register('list', UserListViewSet.UserListViewSet, basename = 'list')
urlpatterns = router.urls

