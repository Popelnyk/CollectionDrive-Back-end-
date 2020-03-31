from rest_framework import serializers, status
from rest_framework.fields import DictField, IntegerField, CharField
from django.db import models
from rest_framework.response import Response

from authapp.models import CustomUser
from collectionapp.models import Collection, Theme


class CollectionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    theme = serializers.CharField(max_length=50)

    class Meta:
        model = Collection
        creation_date = serializers.DateTimeField()
        fields = ['id', 'owner', 'name', 'theme', 'description']

    def create(self, validated_data):
        collection = Collection.objects.create(**validated_data)
        type_description = validated_data.get('theme')

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
