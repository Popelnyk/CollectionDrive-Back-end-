from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from collectionapp.viewsets import CollectionViewSet, ItemViewSet, TagViewSet

router = DefaultRouter()
router.register(r'collections', CollectionViewSet, basename='user')
router.register(r'items', ItemViewSet, basename='items')
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = router.urls

