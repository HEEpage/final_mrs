from django.contrib.auth.forms import UserCreationForm, UserChangeForm #, PasswordChangeForm
from django.contrib.auth import get_user_model
from django import forms

from .models import User, UserMovieLog
from movies.models import MovieGenre


# 회원가입 Form
class CreateUserForm(UserCreationForm) :
    class Meta :
        model = User
        fields = ("email", "username", "password1", "password2", "gender", "birth", "preference_genre")


# 로그인 Form
class LoginUserForm(forms.ModelForm) :
    class Meta :
        model = User
        fields = ["email", "password"]


# 회원 정보 수정 Form
class ChangeUserForm(UserChangeForm) :
    class Meta :
        model = get_user_model()
        fields = ("email", "username", "gender", "birth", "preference_genre")

