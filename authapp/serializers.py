from django.db import models
from rest_framework import serializers
from authapp.models import CustomUser
from collectionapp.models import Collection


class CustomUserSerializer(serializers.ModelSerializer):
    collections = serializers.SerializerMethodField()
    total_collections = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'total_collections', 'collections']

    def get_collections(self, user):
        collections = Collection.objects.filter(owner=user)
        result = []
        for item in collections:
            result.append({'id': item.id, 'name': item.name, 'description': item.description})
        return result

    def get_total_collections(self, user):
        return Collection.objects.filter(owner=user).count()