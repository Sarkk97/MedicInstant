from django.urls import path

from .views import UserSignUp, Users, UserDetail, Login

urlpatterns = [
    path('auth/signup', UserSignUp.as_view(), name="user_sign_up"),
    path('auth/login', Login.as_view(), name="login"),
    path('users', Users.as_view(), name="all_users"),
    path('user/<int:pk>', UserDetail.as_view(), name="user_detail")
]