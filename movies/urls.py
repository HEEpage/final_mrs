from django.urls import path
from movies import views

app_name = 'movies'

urlpatterns = [
    path("", views.movieSearchList, name="search"),
    path("box/", views.movieBoxOfficeList, name="box"),
    path("up/", views.movieUpcomingList, name="up"),
    path("detail/<int:movie_id>/", views.movieDetail, name="detail"),
    path("genre/<int:genre_num>/", views.movieGenreList, name="all_genre"),
    path("genre/<int:genre_num>/<int:sort_num>/", views.movieGenreList, name="one_genre"),
]