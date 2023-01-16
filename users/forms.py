from django.contrib.auth.forms import UserCreationForm, UserChangeForm #, PasswordChangeForm
from django.contrib.auth import get_user_model
from django import forms

from .models import User, UserMovieLog
from movies.models import MovieGenre


# 회원가입 Form
class CreateUserForm(UserCreationForm) :

    GENRE_TYPE = [ (g.type, g.type) for g in MovieGenre.objects.all() ]

    preference_genre = forms.MultipleChoiceField(
        widget = forms.CheckboxSelectMultiple,
        choices = tuple(GENRE_TYPE),
        label = "Preference Genre",
    )

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

    GENRE_TYPE = [ (g.type, g.type) for g in MovieGenre.objects.all() ]

    preference_genre = forms.MultipleChoiceField(
        widget = forms.CheckboxSelectMultiple,
        choices = tuple(GENRE_TYPE),
        label = "Preference Genre",
    )

    class Meta :
        model = get_user_model()
        fields = ['username', 'gender', 'preference_genre']


# 비밀번호 변경 Form
# class PWChangeUserForm(PasswordChangeForm) :
#     model = get_user_model()
#     fields = ['password']