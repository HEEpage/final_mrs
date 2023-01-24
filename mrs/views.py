from django.shortcuts import render
from movies.models import MovieBoxOffice, MovieUpcoming


# Create your views here.
def home(request) :

    up_list = MovieUpcoming.objects.all()
    box_list = MovieBoxOffice.objects.all()
    
    context = {
        "up_list": up_list,
        "box_list": box_list,

    }

    return render(request, "index.html", context)
