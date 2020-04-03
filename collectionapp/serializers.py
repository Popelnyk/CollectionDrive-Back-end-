import jsonfield
from jsonfield.json import JSONString
from rest_framework import serializers, status
from rest_framework.fields import DictField, IntegerField, CharField
from django.db import models
from rest_framework.response import Response
from rest_framework.utils import json

from authapp.models import CustomUser
from collectionapp.models import Collection, Theme, Item
from collectionapp.validators import validate_item_fields


class CollectionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    items = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        creation_date = serializers.DateTimeField()
        fields = ['id', 'owner', 'name', 'theme_name', 'description', 'item_text_fields', 'item_int_fields',
                  'item_bool_fields', 'item_date_fields', 'items']

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
                fields = [{key: value} for key, value in json.loads(fields).items()]
                pass
            else:
                fields = []
            result.append({'name': item.name, 'collection_id': item.collection_id, 'fields': fields})
        return result


class ItemSerializer(serializers.ModelSerializer):
    collection = serializers.ReadOnlyField(source='collection.id')

    class Meta:
        model = Item
        fields = ['id', 'collection', 'name', 'fields']
