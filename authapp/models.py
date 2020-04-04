from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from authapp.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=60, unique=True, null=True)
    email = models.EmailField(_('email address'), max_length=150, unique=True)
    lang = models.CharField(max_length=10, default='en', null=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

