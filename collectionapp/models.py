from django.db import models
from rest_framework.fields import ListField, DictField, CharField, IntegerField, \
    JSONField, BooleanField, DateField

from authapp.models import CustomUser


class Collection(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)
    item_text_fields = models.CharField(max_length=200, null=True)
    item_int_fields = models.CharField(max_length=200, null=True)
    item_bool_fields = models.CharField(max_length=200, null=True)
    item_date_fields = models.CharField(max_length=200, null=True)


class Theme(models.Model):
    collection = models.ManyToManyField(Collection)
    description = models.CharField(max_length=50)


class Item(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    # TODO: Tags
