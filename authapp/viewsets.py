from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from authapp.models import CustomUser
from authapp.serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = CustomUser.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)