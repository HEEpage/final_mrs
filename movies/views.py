from django.shortcuts import render
from django.core.paginator import Paginator
from movies.models import Movie, MovieBoxOffice, MovieUpcoming, MovieWatch
from movies.forms import mvSesarchForm
from django.db.models import Q
# from django.views.generic.edit import FormView
from django.views.generic import DetailView

# Create your views here.
def movieSearchList(request):
    search_list = Movie.objects.all()
    search_key = request.GET.get("search_key") # 검색어 가져오기

    if search_key:
        search_list = search_list.filter(Q(title__icontains=search_key) | Q(director__icontains=search_key) | Q(cast__icontains=search_key)).distinct()

    context = {
        "search_list" : search_list
    }
    return render(request, "movie_list.html", context)

def movieBoxOfficeList(request):
    box_list = MovieBoxOffice.objects.all()
    context = {
        "box_list": box_list
    }
    return render(request, "movie_list.html", context)

def movieUpcomingList(request):
    up_list = MovieUpcoming.objects.all()
    context = {
        "up_list": up_list
    }
    return render(request, "movie_list.html", context)

class movieDetail(DetailView):
    model = MovieWatch
    template_name = "movie_datil.html"


# def index(request):
#     page = request.GET.get('page', '1')  # 페이지
#     movie_list = Movie.objects.order_by('-release_date')
#     paginator = Paginator(movie_list, 10)  # 페이지당 10개씩 보여주기
#     page_obj = paginator.get_page(page)
#     context = {'movie_list': page_obj}
#     return render(request, 'templates/movie_list.html', movie_list)