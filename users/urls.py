from django.urls import path
from django.contrib.auth import views as auth_views

from .views import UserCreateView

app_name = 'users'

urlpatterns = [
    path("signup/", UserCreateView.as_view(), name = "signup"), # 회원가입
    path("signin/", auth_views.LoginView.as_view(template_name="users/signin.html"), name = "signin"), # 로그인
    path("signout/", auth_views.LogoutView.as_view(), name = "signout"), # 로그아웃
    
]