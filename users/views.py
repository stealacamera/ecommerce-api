from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, UpdateAPIView

from .models import Address
from . import serializers


class RegisterView(APIView):
    def post(self, request):
        serialized = serializers.RegisterSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        
        account = serialized.save()
        tokens = RefreshToken.for_user(account)
        
        data = {'username': account.username,
                'email': account.email,
                'Registration successful': f'Welcome, {account.username}!',
                'tokens': {'refresh': str(tokens),
                           'access': str(tokens.access_token)}}
        
        return Response(data, status=status.HTTP_201_CREATED)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        serialized = serializers.ChangePasswordSerializer(data=request.data,
                                                          context = {'request': request})
        serialized.is_valid(raise_exception=True)
        serialized.save()
        
        return Response('Password changed successfully, please log back in',
                        status=status.HTTP_200_OK)

class ChangeAddress(UpdateAPIView):
    serializer_class = serializers.AddressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return Address.objects.get(user=self.request.user)

class CurrentProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serialized = serializers.CurrentProfileSerializer(self.request.user,
                                                          context = {'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        serialized = serializers.ChangeUsernameSerializer(data=request.data,
                                                          context = {'request': request})
        serialized.is_valid(raise_exception=True)
        serialized.save()
        
        return Response('Username changed successfully', status=status.HTTP_200_OK)

class ProfileView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.ProfileSerializer
    
    lookup_field = 'username'
    lookup_url_kwarg = 'username'