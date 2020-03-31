from django.db import models
from rest_framework.fields import ListField, DictField, CharField, IntegerField, JSONField

from authapp.models import CustomUser


class Collection(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)
    #item_fields = JSONField()


class Theme(models.Model):
    collection = models.ManyToManyField(Collection)
    description = models.CharField(max_length=50)

