from django.shortcuts import render, redirect
from movies.models import Movie, MovieBoxOffice, MovieUpcoming, MovieWatch
from django.db.models import Q
from django.views.generic import DetailView
from movies.genre_type import GENRE_TYPE

# Create your views here.
def movieGenreList(request, genre_num): # sort_num=None
    genre_num = int(request.POST.get('genre_num')) - 1
    # sort_num = request.POST.get('sort_num')
    print('genre_num : ', genre_num - 1)
    # print('sort_num : ', sort_num)

    gen_list = Movie.objects.filter(genre__contains=GENRE_TYPE[genre_num])

    # if sort_num == 1: # 장르 필터링 + 클릭수가 많은 순
    #     gen_list = Movie.objects.filter(genre__contains=GENRE_TYPE[genre_num]).order_by(-cnt_click)
    # elif sort_num == 2: # 장르 필터링 + 최신순
    #     gen_list = Movie.objects.filter(genre__contains=GENRE_TYPE[genre_num]).order_by(-release_date)
    # elif sort_num == None: # 장르 필터링
    #     gen_list = Movie.objects.filter(genre__contains=GENRE_TYPE[genre_num])

    context = {
        'genre_type': GENRE_TYPE,
        'genre_num': genre_num,
        # 'sort_num': sort_num,
        'gen_list': gen_list
    }
    # redirect('genre/<int:genre_num>')
    return render(request, 'movies/movie_list.html', context)

def movieSearchList(request):
    search_list = Movie.objects.all()
    search_key = request.GET.get("search_key") # 검색어 가져오기

    if search_key:
        search_list = search_list.filter(Q(title__icontains=search_key) | Q(director__icontains=search_key) | Q(cast__icontains=search_key)).distinct()

    context = {
        "search_list" : search_list,
        "genre_type": GENRE_TYPE
    }
    return render(request, "movies/movie_list.html", context)

def movieBoxOfficeList(request):
    box_list = MovieBoxOffice.objects.all()
    print(box_list)
    context = {
        "box_list": box_list
    }
    return render(request, "movies/movie_list.html", context)

def movieUpcomingList(request):
    up_list = MovieUpcoming.objects.all()
    print(up_list)
    context = {
        "up_list": up_list
    }
    return render(request, "movies/movie_list.html", context)

def movieDetail(request):
    model = Movie
    template_name = 'movies/movie_detail.html'