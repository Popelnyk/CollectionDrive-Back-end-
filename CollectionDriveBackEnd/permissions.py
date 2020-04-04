from rest_framework import permissions, status
from rest_framework.response import Response

from collectionapp.models import Collection, Item


class IsOwnerOfUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class IsOwnerOfCollectionOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            collection_id = view.kwargs['pk']
            collection = Collection.objects.get(id=collection_id)

            return collection.owner == request.user
        except Exception as e:
            return Response('collection does not exist', status=status.HTTP_400_BAD_REQUEST)


class IsOwnerAndCanCreateItems(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            item_id = view.kwargs['pk']
            item = Item.objects.get()

            return item.collection.owner == request.user
        except Exception as e:
            return Response('item does not exist', status=status.HTTP_400_BAD_REQUEST)