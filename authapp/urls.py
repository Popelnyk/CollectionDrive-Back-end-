from allauth.account.views import confirm_email
from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from authapp.viewsets import CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = router.urls
urlpatterns += [
    url(r'^token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
