from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "users"

urlpatterns = [

    path("register/", views.UserCreateView.as_view(), name = "register"), # 회원가입
    path("update/", views.update, name = "update"), # 회원 정보 수정
    # path("password/", password, name = "password"), # 비밀번호 변경
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name = "login"), # 로그인
    path("logout/", auth_views.LogoutView.as_view(), name = "logout"), # 로그아웃

    path("", views.UserPageView.as_view(), name = "user_page"), # 마이 페이지

    path("mv-log/", views.user_mvlog_view, name = "user_mvlog"), # 영화 기록 - 목록 확인
    path("mv-log/search/", views.user_mvlog_search_view, name = "user_mvlog_search"), # 영화 기록 - 작성할 영화 검색
    path("mv-log/add/", views.user_mvlog_add_view, name = "user_mvlog_add"), # 영화 기록 - 등록
    path("mv-log/write/", views.user_mvlog_write_view, name = "user_mvlog_write"), # 영화 기록 - 작성
    path("mv-log/delete/<int:no>", views.user_mvlog_delete_view, name = "user_mvlog_delete"), # 영화 기록 - 삭제

    path("wish/", views.UserWishView.as_view(), name = "user_wish"), # 위시리스트
    path("wish/delete/<int:no>", views.user_wish_delete_view, name = "user_wish_delete"), # 위시리스트 삭제

]