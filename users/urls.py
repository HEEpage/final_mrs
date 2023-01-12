from django.urls import path, include

from .views import UserCreateView

app_name = 'users'

urlpatterns = [
    path("signup/", UserCreateView.as_view(), name = "signup"), # 회원가입
]