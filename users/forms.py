from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User

# 선호 장르 선택
CHOICES_GENRE = ( ("드라마", "드라마"), ("판타지", "판타지"), ("서부", "서부"), ("공포", "공포"), 
                ("멜로/로맨스", "멜로/로맨스"), ("모험", "모험"), ("스릴러", "스릴러"), ("느와르", "느와르"), 
                ("컬트", "컬트"), ("다큐멘터리", "다큐멘터리"), ("코미디", "코미디"), ("가족", "가족"),
                ("미스터리", "미스터리"), ("전쟁", "전쟁"), ("애니메이션", "애니메이션"), ("범죄", "범죄"),
                ("뮤지컬", "뮤지컬"), ("SF", "SF"), ("액션", "액션"), ("무협", "무협"), ("에로", "에로"),
                ("서스펜스", "서스펜스"), ("서사", "서사"), ("블랙코미디", "블랙코미디"), ("실험", "실험"), 
                ("공연실황", "공연실황"),
    )

# 회원가입 Form
class CreateUserForm(UserCreationForm) :

    preference_genre = forms.MultipleChoiceField(
        widget = forms.CheckboxSelectMultiple,
        choices = CHOICES_GENRE,
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

