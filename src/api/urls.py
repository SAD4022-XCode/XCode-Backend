from rest_framework import routers
from .views import *  

router = routers.DefaultRouter()

router.register('account', UserProfileViewSet, basename = 'account')
router.register('', UserListViewSet.UserListViewSet, basename = 'list')
urlpatterns = router.urls

