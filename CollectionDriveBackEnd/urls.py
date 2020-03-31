from allauth.account.views import confirm_email
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

import authapp
from authapp.viewsets import CustomUserViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    url('auth/', include('authapp.urls')),
    url('collections/', include('collectionapp.urls'))
]
