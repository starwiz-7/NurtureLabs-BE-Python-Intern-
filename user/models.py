from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
# Create your models here.

class Manager(BaseUserManager):
    def create_user(self,email,name,password=None):
        if not email:
            raise ValueError('user must have email address')

        user = self.model( email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,name,password=None):
        if not email:
            raise ValueError('user must have email address')

        if not password:
            raise ValueError("User must have password")

        user = self.create_user(email=self.normalize_email(email),name=name,password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = Manager()

    def __str__(self):
        return self.email

    def create_token(self):
        token = RefreshToken.for_user(self)
        return {'refresh':str(token),'access':str(token.access_token)}

    