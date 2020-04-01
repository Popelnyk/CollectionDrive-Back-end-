from rest_framework import permissions

from collectionapp.models import Collection


class IsOwnerOfUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class IsOwnerOfCollectionOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        collection_id = view.kwargs['pk']
        collection = Collection.objects.get(id=collection_id)

        return collection.owner == request.user
