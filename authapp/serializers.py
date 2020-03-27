from django.db import models
from rest_framework import serializers
from authapp.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'spouse_name', 'date_of_birth']