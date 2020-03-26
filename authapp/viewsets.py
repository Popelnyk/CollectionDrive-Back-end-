from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from authapp.models import CustomUser
from authapp.serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid() and request.data['password']:
            user = CustomUser.objects.create_user(username=request.data['username'],
                                                  email=request.data['email'],
                                                  password=request.data['password'])
            return Response({'id': user.id, 'username': user.username, 'email': user.email})
        elif not request.data['password']:
            return Response(data={'Error': 'The Password must be set'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
