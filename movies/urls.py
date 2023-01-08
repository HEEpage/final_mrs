from django.urls import path
from movies import views

app_name = 'movies'

urlpatterns = [
    # path('', views.movieSearchList, name='movie_sl'),
    path("", views.movieSearchList, name="search"),
    path("box/", views.movieBoxOfficeList, name="box"),
    path("up/", views.movieUpcomingList, name="up"),
    path("detail/<int:movie_id>", views.movieDetail.as_view(), name="detail"),
]