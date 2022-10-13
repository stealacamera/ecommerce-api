from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['id', 'user']


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()
    address = AddressSerializer()
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 
                  'password', 'password2', 'address']
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is taken')
        
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is in use by another account')
        
        return value
    
    def save(self):
        password = self.validated_data['password']
        address_data = self.validated_data['address']
        
        if password != self.validated_data['password2']:
            raise serializers.ValidationError('Passwords have to match')
        
        account = User.objects.create_user(username=self.validated_data['username'],
                                           email=self.validated_data['email'],
                                           first_name=self.validated_data['first_name'],
                                           last_name=self.validated_data['last_name'])
        account.set_password(password)
        account.save()
        
        address = Address.objects.create(user=account,
                                         country=address_data['country'],
                                         city=address_data['city'],
                                         street_address=address_data['street_address'],
                                         zip_code=address_data['zip_code'])
        address.save()
        
        return account


class ChangeUsernameSerializer(serializers.Serializer):
    new_username = serializers.CharField()
    
    def validate_new_username(self, value):
        if self.context['request'].user.username == value:
            raise serializers.ValidationError('New username should be different from current one')
        
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is taken')
        
        return value
    
    def save(self):
        account = self.context['request'].user
        account.username = self.validated_data['new_username']
        account.save()


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    refresh = serializers.CharField()
    
    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect')
        
        return value
    
    def validate(self, attrs):
        self.refresh_token = attrs['refresh']
        return super().validate(attrs)
    
    def save(self):
        try:
            new_password = self.validated_data['new_password']
            account = self.context['request'].user
            
            if new_password == self.validated_data['current_password']:
                raise serializers.ValidationError('New password should be different from current one')
            
            account.set_password(new_password)
            account.save()
            RefreshToken(self.refresh_token).blacklist()
        except TokenError:
            raise serializers.ValidationError('Token is invalid or expired')


class CurrentProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    products = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='product-detail')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'products']


class ProfileSerializer(serializers.ModelSerializer):
    products = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='product-detail')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'products']