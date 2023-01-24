from django.urls import path
from api import views


app_name = 'api'
urlpatterns = [

    # movies 관련
    path('movies/list', views.MovieListAPI.as_view(), name='movie_list'),
    path('movies', views.MovieDetailAPI.as_view(), name='movie_detail'),
    path('movies/review/list', views.ReviewDummyListAPI.as_view(), name='review_dummy_list'),
    path('movies/review/', views.UserMovieLogAPI.as_view(), name='review_list'),

    # accounts 관련
    path('accounts/review/', views.UserLogAPI.as_view(), name='review_list'),
    path('accounts/review/<int:no>', views.UserLogDetailAPI.as_view(), name='review_detail'),
    path('accounts/wish/', views.UserWishAPI.as_view(), name='wishlist'),
    path('accounts/wish/<int:no>', views.UserWishDetailAPI.as_view(), name='wish_detail'),

    # 기연 - api 추가
    path('accounts/', views.UserAPI.as_view(), name='user_info'),
    path('accounts/wish/status', views.UserWishStatusAPI.as_view(), name = 'wish_status'),
    path('accounts/review/status', views.UserReviewStatusAPI.as_view(), name = 'review_status'),

]