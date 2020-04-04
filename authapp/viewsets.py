from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets, status, permissions, mixins
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

from authapp.models import CustomUser
from authapp.serializers import CustomUserSerializer
from CollectionDriveBackEnd.permissions import IsOwnerOfUserOrReadOnly


class CustomUserViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        try:
            if serializer.is_valid() and request.data['password']:
                user = CustomUser.objects.create_user(username=request.data['username'],
                                                      email=request.data['email'],
                                                      password=request.data['password'])
                return Response({'id': user.id, 'username': user.username, 'email': user.email, 'lang': user.lang},
                                status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MultiValueDictKeyError as e:
            return Response(data={'password and lang': 'These fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsOwnerOfUserOrReadOnly])
    def set_password(self, request, pk):
        user = self.get_object()
        try:
            if request.data['password1'] == request.data['password2'] and len(request.data['password1']) >= 8:
                user.set_password(request.data['password1'])
                return Response(data={'password': 'New password was successfully set'}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(data={'passwords do not match or password\'s length is less than 8'},
                                status=status.HTTP_400_BAD_REQUEST)
        except MultiValueDictKeyError as e:
            return Response(data={'password1': 'This field is required', 'password2': 'This field is required'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsOwnerOfUserOrReadOnly])
    def set_username(self, request, pk):
        user = self.get_object()
        try:
            if CustomUser.objects.filter(username=request.data['username']).count() == 0:
                user.username = request.data['username']
                user.save()
                return Response(data={'username': user.username}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(data={'username': 'this username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except MultiValueDictKeyError as e:
            return Response(data={'username': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)
