from rest_framework.routers import DefaultRouter

from authapp.viewsets import CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
urlpatterns = router.urls
