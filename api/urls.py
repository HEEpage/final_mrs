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

]