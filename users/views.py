from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in

from rest_framework import generics, status

from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, LoginSerializer

# Create your views here.
class UserSignUp(generics.CreateAPIView):
    serializer_class = UserSerializer

class Users(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(is_active=True)

class Login(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user_id = response.data.get('user')["id"]
        user = get_user_model().objects.get(pk=user_id)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        return response
