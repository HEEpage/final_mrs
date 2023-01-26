from django.urls import path
from movies import views

app_name = 'movies'

urlpatterns = [
    path("", views.MovieSearchList.as_view(), name="search"),
    path("detail/<int:movie_id>/", views.movieDetail, name="detail"),
    path("genre/<int:genre_num>/", views.MovieGenreList.as_view(), name="all_genre"),

    # path("genre/recom/", views.return_recom),

]