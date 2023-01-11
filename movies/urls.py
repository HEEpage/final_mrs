from django.urls import path
from movies import views

app_name = 'movies'

urlpatterns = [
    path("", views.movieSearchList, name="search"),
    path("box/", views.movieBoxOfficeList, name="box"),
    path("up/", views.movieUpcomingList, name="up"),
    path("detail/<int:movie_id>", views.movieDetail, name="detail"),
    path("/movies/genre/<int:genre>", views.movieGenreList, name="all_genre"),
    path("/movies/genre/<int:genre>/<int:sort>", views.movieGenreList, name="one_genre"),
]