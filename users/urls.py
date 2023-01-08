from django.urls import path, include

from .views import UserCreateView

app_name = 'users'

urlpatterns = [
    # django.contrib.auth.urls 장고 내장 인증 urls 활용
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", UserCreateView.as_view(), name = "register"), # 회원가입
]