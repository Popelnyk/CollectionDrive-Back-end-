from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from collectionapp.viewsets import CollectionViewSet, ItemViewSet

router = DefaultRouter()
router.register(r'collections', CollectionViewSet, basename='user')
router.register(r'items', ItemViewSet, basename='items')

urlpatterns = router.urls

