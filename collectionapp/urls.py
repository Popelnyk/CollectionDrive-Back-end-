from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from collectionapp.viewsets import CollectionViewSet


router = DefaultRouter()
router.register(r'', CollectionViewSet, basename='user')

urlpatterns = router.urls
