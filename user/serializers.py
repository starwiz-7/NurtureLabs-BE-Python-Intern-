from .models import User
from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100,min_length=8, write_only=True)
    id = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = ['id','email','name','password']
    
    def validate(self, attrs):
        email = attrs.get('email')
        name = attrs.get('name')
        return attrs
    
    def create(self,data):
        return User.objects.create_user(**data)


class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    password=serializers.CharField(max_length=100,min_length=8,write_only=True)
    tokens=serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id','email','password','tokens']
    
    def validate(self,attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')

        user = auth.authenticate(email=email,password=password)
        if not user:
            raise AuthenticationFailed('Invalid Credentials')
        return {
            'email':user.email,
            'tokens':user.create_token,
            'id':user.id
        }