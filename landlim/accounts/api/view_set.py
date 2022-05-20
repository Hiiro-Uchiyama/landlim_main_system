from django.contrib.auth import authenticate
from django.db import transaction
from django.http import HttpResponse, Http404
from rest_framework import authentication, permissions, generics
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from .serializer import AccountSerializer
from ..models import User, UserManager

## API to create users
class AuthSignUp(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    @transaction.atomic
    def post(self, request, format=None):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## View of user information acquisition
class AuthInfoGetView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    def get(self, request, format=None):
        return Response(data={
            'username': request.user.username,
            'email': request.user.email,
            'profile': request.user.profile,
        },
            status=status.HTTP_200_OK)

class AuthInfoUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AccountSerializer
    lookup_field = 'email'
    queryset = User.objects.all()

    def get_object(self):
        try:
            instance = self.queryset.get(email=self.request.user)
            return instance
        except User.DoesNotExist:
            raise Http404