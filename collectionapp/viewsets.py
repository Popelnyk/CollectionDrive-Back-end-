from json import JSONDecodeError

import jsonfield
from rest_framework import viewsets, mixins, permissions, status, filters
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response
from rest_framework.utils import json

from CollectionDriveBackEnd.permissions import IsOwnerOfCollectionOrReadonly, IsOwnerAndCanCreateItems, IsOwnerOfComment
from collectionapp.helpfuncs import create_or_add_tags
from collectionapp.models import Collection, Item, Comment, Tag
from collectionapp.serializers import CollectionSerializer, ItemSerializer, CommentSerializer, TagSerializer
from collectionapp.validators import validate_fields_from_request_to_fields_in_collection, validate_tags


class CollectionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()
    search_fields = ['name', 'theme_name', 'description', 'item__name', 'item__tags', 'item__comment__description']
    filter_backends = (filters.SearchFilter,)

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
                validated_tags = validate_tags(json.loads(request.data['tags']))

                if not validated[0]:
                    return Response(validated[1], status=status.HTTP_400_BAD_REQUEST)

                if not validated_tags[0]:
                    return Response(validated_tags[1], status=status.HTTP_400_BAD_REQUEST)

                item = Item.objects.create(collection=collection, name=request.data['name'],
                                           tags=request.data['tags'], fields=request.data['fields'])

                create_or_add_tags(request.data['tags'], item)

                data_for_response = {'name': request.data['name'], 'tags': json.loads(request.data['tags']),
                                     'fields': json.loads(request.data['fields'])}

                return Response({'id': item.id, 'collection_id': collection.id, 'data': data_for_response},
                                status=status.HTTP_201_CREATED)
            except JSONDecodeError as e:
                return Response('Incorrect <fields> atr in request', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def best(self, request):
        collections = Collection.objects.all()
        result_bad = sorted(collections, key=lambda collection: Item.objects.filter(collection=collection).count())
        result = []
        for item in result_bad:
            result.append({'id': item.id, 'name': item.name, 'theme': item.theme_name,
                           'description': item.description, 'creation_date': item.creation_date,
                           'total_of_items': Item.objects.filter(collection=item).count()})
        return Response(reversed(result), status=status.HTTP_200_OK)


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
            item = Item.objects.get(id=pk)

            comment = Comment.objects.create(owner=self.request.user, item=item,
                                             description=request.data['description'])

            return Response({'id': comment.id, 'owner': comment.owner.username, 'owner_id': comment.owner_id,
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


class TagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def retrieve(self, request, *args, **kwargs):
        tag = Tag.objects.get(id__exact=kwargs['pk'])

        result = []
        for item in tag.item.all():
            result.append({'name': item.name, 'fields': json.loads(item.fields), 'tags': json.loads(item.tags)})

        return Response(result, status=status.HTTP_200_OK)

