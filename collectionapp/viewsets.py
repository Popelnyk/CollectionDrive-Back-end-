from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from collectionapp.models import Collection
from collectionapp.serializers import CollectionSerializer


class CollectionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'delete':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]