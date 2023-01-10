from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from movies.models import Movie


# 사용자 정보 테이블
class User(AbstractUser) :
    
    email = models.EmailField(
        unique = True,
        primary_key = True,
        error_messages = {
            "unique" : "입력한 E-mail이 이미 존재합니다.",
        },
    ) # 사용자 E-mail

    password = models.CharField(max_length=255) # 패스워드

    username = models.CharField(
        max_length = 30,
        unique = True,
        error_messages = {
            "unique" : "입력한 닉네임이 이미 존재합니다.",
        },
    ) # 닉네임

    GENDER_MALE = "m"
    GENDER_FEMALE = "f"
    CHOICES_GENDER = ( (GENDER_MALE, "male"), (GENDER_FEMALE, "female") )

    gender = models.CharField(max_length = 1, choices = CHOICES_GENDER) # 성별
    birth = models.DateField() # 생년월일
    preference_genre = models.CharField(max_length = 50) # 선호 장르

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "gender", "birth", "preference_genre"]

    def __str__(self) :
        return f"{self.email} -- {self.username}"


# 사용자-영화 관람 기록 테이블
class UserMovieLog(models.Model) :
    
    no = models.BigAutoField(primary_key=True) # 번호

    user_email = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        db_column = "user_email",
    ) # 사용자 E-mail
    movie_id = models.ForeignKey(Movie, on_delete = models.CASCADE, db_column = "movie_id") # 영화 고유 ID

    grade = models.FloatField() # 평점
    review = models.CharField(max_length = 300, blank = True) # 리뷰
    c_date = models.DateTimeField(auto_now_add=True) # 기록 작성일

    def __str__(self) :
        return f"{self.pk} -- {self.user_email} -- {self.movie_id} -- {self.grade}"


# 사용자 페이지 사용 기록 테이블 (영화 상세페이지 클릭하면 자동 기록)
class UserLogData(models.Model) :
    
    no = models.BigAutoField(primary_key=True) # 번호

    user_email = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        db_column = "user_email",
    ) # 사용자 E-mail
    movie_id = models.ForeignKey(Movie, on_delete = models.CASCADE, db_column = "movie_id") # 영화 고유 ID

    log_date = models.DateTimeField(auto_now_add=True) # 기록 작성일

    def __str__(self) :
        return f"{self.pk} -- {self.user_email} -- {self.movie_id} -- {self.log_date}"


# 사용자 위시리스트
class UserMovieWish(models.Model) :

    no = models.BigAutoField(primary_key=True) # 번호

    user_email = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        db_column = "user_email",
    ) # 사용자 E-mail
    movie_id = models.ForeignKey(Movie, on_delete = models.CASCADE, db_column = "movie_id") # 영화 고유 ID

    def __str__(self) :
        return f"{self.pk} -- {self.user_email} -- {self.movie_id}"

