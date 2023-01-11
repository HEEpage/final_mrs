from django.shortcuts import render
from movies.models import Movie, MovieBoxOffice, MovieUpcoming, MovieWatch
from django.db.models import Q
from django.views.generic import DetailView

# Create your views here.
def movieGenreList(request):
    genre_num = request.GET.get('genre')
    print(genre_num)

    GENRE_TYPE = ["드라마", "판타지", "서부", "공포", "멜로/로맨스", "모험", "스릴러", "느와르", "컬트", "다큐멘터리", "코미디", "가족", "미스터리", "전쟁", "애니메이션", "범죄", "뮤지컬", "SF", "액션", "무협", "에로", "서스펜스", "서사", "블랙코미디", "실험", "공연실황"]
    gen_list = Movie.objects.filter(genre__contains=GENRE_TYPE[genre_num])

    context = {
        'genre_num': genre_num,
        'gen_list': gen_list
    }
    return render(request, 'movies/movie_list.html', context)

def movieSearchList(request):
    search_list = Movie.objects.all()
    search_key = request.GET.get("search_key") # 검색어 가져오기

    if search_key:
        search_list = search_list.filter(Q(title__icontains=search_key) | Q(director__icontains=search_key) | Q(cast__icontains=search_key)).distinct()

    context = {
        "search_list" : search_list
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