from json import JSONDecodeError

import jsonfield
from jsonfield.json import JSONString
from rest_framework import serializers, status
from rest_framework.fields import DictField, IntegerField, CharField
from django.db import models
from rest_framework.response import Response
from rest_framework.utils import json

from authapp.models import CustomUser
from collectionapp.models import Collection, Theme, Item, Comment, Tag
from collectionapp.validators import validate_item_fields, validate_tags


class CollectionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_id = serializers.ReadOnlyField(source='owner.id')
    items = serializers.SerializerMethodField()
    total_of_items = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        creation_date = serializers.DateTimeField(format='%Y-%m-%d')
        fields = ['id', 'owner', 'owner_id', 'name', 'theme_name', 'description', 'creation_date',
                  'item_text_fields', 'item_int_fields', 'item_bool_fields',
                  'item_date_fields', 'total_of_items', 'items']

    def to_representation(self, collection):
        serialized_data = super(CollectionSerializer, self).to_representation(collection)
        serialized_data['item_text_fields'] = json.loads(collection.item_text_fields)
        serialized_data['item_int_fields'] = json.loads(collection.item_int_fields)
        serialized_data['item_bool_fields'] = json.loads(collection.item_bool_fields)
        serialized_data['item_date_fields'] = json.loads(collection.item_date_fields)
        return serialized_data

    def create(self, validated_data):
        validate_item_fields(json.loads(validated_data.get('item_text_fields')))
        validate_item_fields(json.loads(validated_data.get('item_int_fields')))
        validate_item_fields(json.loads(validated_data.get('item_bool_fields')))
        validate_item_fields(json.loads(validated_data.get('item_date_fields')))

        collection = Collection.objects.create(**validated_data)
        type_description = validated_data.get('theme_name')

        if Theme.objects.filter(description__exact=type_description).count() > 0:
            theme = Theme.objects.get(description__exact=type_description)
            theme.collection.add(collection)
            theme.save()
        else:
            Theme.objects.create(description=type_description)
            theme = Theme.objects.get(description__exact=type_description)
            theme.collection.add(collection)
            theme.save()

        return collection

    def get_items(self, collection):
        items = Item.objects.filter(collection=collection)
        result = []
        for item in items:
            fields = item.fields
            if isinstance(fields, JSONString):
                fields = json.loads(fields)
            result.append({'id': item.id, 'name': item.name, 'collection_id': item.collection_id, 'fields': fields})
        return result

    def get_total_of_items(self, collection):
        return Item.objects.filter(collection=collection).count()


class ItemSerializer(serializers.ModelSerializer):
    collection = serializers.ReadOnlyField(source='collection.id')
    fields_repr = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    tags = serializers.CharField(max_length=500, allow_null=True)
    tags_repr = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'collection', 'name', 'fields', 'fields_repr', 'comments', 'tags', 'tags_repr']

    def create(self, validated_data):
        item = Item.objects.create(**validated_data)

        try:
            tags_from_json = json.loads(validated_data.get('tags'))
        except JSONDecodeError as e:
            return Response('incorrect tags, must be [{name:<tag_name>},...]', status=status.HTTP_400_BAD_REQUEST)

        validated = validate_tags(tags_from_json)
        if not validated[0]:
            return Response(validated[1], status=status.HTTP_400_BAD_REQUEST)

        for data in tags_from_json:
            data['name'] = str.lower(data['name'])
            if Tag.objects.filter(name__exact=data['name']).count() > 0:
                tag = Tag.objects.get(name__exact=data['name'])
                tag.item.add(item)
                tag.save()
            else:
                Tag.objects.create(name=data['name'])
                tag = Tag.objects.get(name__exact=data['name'])
                tag.item.add(item)
                tag.save()

        return item

    def get_fields_repr(self, item):
        return json.loads(item.fields)

    def get_tags_repr(self, item):
        if item.tags:
            return json.loads(item.tags)
        else:
            return []

    def get_comments(self, item):
        result = []
        comments = Comment.objects.filter(item=item)
        for data in comments:
            result.append({'id': data.id, 'owner': data.owner, 'owner_id': data.owner_id,
                           'description': data.description, 'creation_date': data.creation_date})
        return result


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_id = serializers.ReadOnlyField(source='owner.id')
    item = serializers.ReadOnlyField(source='item.id')

    class Meta:
        model = Comment
        creation_date = serializers.DateTimeField(format='%Y-%m-%d')
        fields = ['id', 'owner', 'item', 'description', 'creation_date']
