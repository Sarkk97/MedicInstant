from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import CustomUserManager
# Create your models here.

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.ForeignKey('Role', models.SET_NULL, null=True, related_name="users")
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.first_name+' '+self.last_name or self.email

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
#class Pharmacy(models.Model)