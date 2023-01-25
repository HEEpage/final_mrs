from django.shortcuts import render
from movies.models import MovieBoxOffice, MovieUpcoming, MovieGenre


# Create your views here.
def home(request) :

    up_list = MovieUpcoming.objects.all()
    box_list = MovieBoxOffice.objects.all()
    
    context = {
        "up_list": up_list,
        "box_list": box_list,

    }

    # ----------- 추가 ------------
    genre_list = MovieGenre.objects.all()
    length = len(genre_list)//2 + 1

    context["genre_type1"] = genre_list[:length]
    context["genre_type2"] = genre_list[length:]
    # ----------- 끝 ------------

    return render(request, "index.html", context)
