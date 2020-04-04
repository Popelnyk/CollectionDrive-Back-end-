from json import JSONDecodeError

import jsonfield
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response
from rest_framework.utils import json

from CollectionDriveBackEnd.permissions import IsOwnerOfCollectionOrReadonly, IsOwnerAndCanCreateItems, IsOwnerOfComment
from collectionapp.models import Collection, Item, Comment
from collectionapp.serializers import CollectionSerializer, ItemSerializer, CommentSerializer
from collectionapp.validators import validate_fields_from_request_to_fields_in_collection


class CollectionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy' or self.action == 'update':
            permission_classes = [IsOwnerOfCollectionOrReadonly]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        try:
            collection = Collection.objects.get(id=kwargs['pk'])
            collection.delete()
            return Response('deleted', status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response('collection does not exist', status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, permission_classes=[IsOwnerOfCollectionOrReadonly])
    def create_item(self, request, pk=None):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            try:
                collection = Collection.objects.get(id=pk)
                validated = validate_fields_from_request_to_fields_in_collection(collection, json.loads(request.data['fields']))

                if not validated[0]:
                    return Response(validated[1], status=status.HTTP_400_BAD_REQUEST)

                data_for_response = [request.data['name'], json.loads(request.data['fields'])]
                item = Item.objects.create(collection=collection, name=request.data['name'], fields=request.data['fields'])

                return Response({'id': item.id, 'collection_id': collection.id, 'data': data_for_response},
                                status=status.HTTP_201_CREATED)
            except JSONDecodeError as e:
                return Response('Incorrect <fields> atr in request', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsOwnerAndCanCreateItems]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        try:
            item = Item.objects.get(id=kwargs['pk'])
            item.delete()
            return Response('deleted', status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response('item does not exist', status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            item = Item.objects.get(id='pk')
            comment = Comment.objects.create(owner=self.request.user, item=item,
                                   description=request.data['description'])
            return Response({'id':comment.id, 'owner':comment.owner, 'owner_id':comment.owner_id,
                             'description': comment.description, 'creation_date': comment.creation_date},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=True, permission_classes=[IsOwnerOfComment])
    def delete_comment(self, request, pk=None):
        try:
            comment = Comment.objects.get(id='pk')
            comment.delete()
            return Response('deleted', status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response('comment does not exist', status=status.HTTP_400_BAD_REQUEST)
