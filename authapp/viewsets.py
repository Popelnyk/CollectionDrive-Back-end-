from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from authapp.models import CustomUser
from authapp.serializers import CustomUserSerializer
from CollectionDriveBackEnd.permissions import IsOwnerOfUserOrReadOnly


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

    @action(detail=True, methods=['post'], permission_classes=[IsOwnerOfUserOrReadOnly])
    def set_password(self, request, pk):
        user = self.get_object()
        if request.data['password1'] == request.data['password2'] and len(request.data['password1']) >= 8:
            user.set_password(request.data['password1'])
            return Response(data='Password was successfully set', status=status.HTTP_202_ACCEPTED)
        elif len(request.data['password1']) < 8:
            return Response(data='Password must have at least 8 symbols', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data='Passwords do not match', status=status.HTTP_400_BAD_REQUEST)

