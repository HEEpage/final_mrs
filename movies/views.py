from django.shortcuts import render, redirect
from movies.models import Movie, MovieBoxOffice, MovieUpcoming, MovieWatch, MovieReviewDummy, MovieGenre
from django.db.models import Q
from django.views.generic import DetailView
from users.models import User, UserMovieWish

# Create your views here.
# 영화 장르 필터링 및 정렬
def movieGenreList(request, genre_num, sort_num=None): # 
    genre_num = request.POST.get('genre_num')
    # print('genre_num : ', genre_num) # int
    genre_type = MovieGenre.objects.get(pk=genre_num)
    genre_all = MovieGenre.objects.all()

    sort_num = request.POST.get('sort_num')

    gen_list = Movie.objects.filter(genre__contains=genre_type.type)
    # print(gen_list)

    # if sort_num == 1: # 장르 필터링 + 클릭수가 많은 순
    #     gen_list = Movie.objects.filter(genre__contains=GENRE_TYPE[genre_num]).order_by(-cnt_click)
    # elif sort_num == 2: # 장르 필터링 + 최신순
    #     gen_list = Movie.objects.filter(genre__contains=GENRE_TYPE[genre_num]).order_by(-release_date)
    # elif sort_num == None: # 장르 필터링
    #     gen_list = Movie.objects.filter(genre__contains=GENRE_TYPE[genre_num])

    context = {
        'genre_num': genre_num,
        'genre_type': genre_all,
        'sort_num': sort_num,
        'gen_list': gen_list
    }
    
    return render(request, 'movies/movie_list.html', context)

# 영화 검색
def movieSearchList(request):
    search_list = Movie.objects.all()
    search_key = request.GET.get("search_key") # 검색어 가져오기
    genre_type = MovieGenre.objects.all()

    if search_key:
        search_list = search_list.filter(Q(title__icontains=search_key) | Q(director__icontains=search_key) | Q(cast__icontains=search_key)).distinct()

    context = {
        "search_list" : search_list,
        "genre_type": genre_type,
    }
    return render(request, "movies/movie_list.html", context)

# 영화 현재 상영작 목록 보기
def movieBoxOfficeList(request):
    box_list = MovieBoxOffice.objects.all()
    print(box_list)
    context = {
        "box_list": box_list
    }
    return render(request, "movies/movie_list.html", context)

# 영화 개봉 예정작 목록 보기
def movieUpcomingList(request):
    up_list = MovieUpcoming.objects.all()
    print(up_list)
    context = {
        "up_list": up_list
    }
    return render(request, "movies/movie_list.html", context)

# 영화 상세 정보 보기
def movieDetail(request, movie_id):
    movie_detail = Movie.objects.get(id=movie_id)
    movie_review = MovieReviewDummy.objects.filter(movie_id=movie_id)
    
    if movie_detail.status != 2:
        movie_watch = MovieWatch.objects.get(movie_id=movie_id)
    else:
        movie_watch = []

    if request.POST:
        user_email = request.user.email
        print(user_email)

        wish_movie = request.POST.get('wish')
        print("get wish >> ", wish_movie)

        if wish_movie : 
            print("front save")
            already_wish = UserMovieWish.objects.filter(movie_id = wish_movie).count()
            if(already_wish == 0):
                wish = {
                    "user_email" : User.objects.get(email = request.user.email),
                    "movie_id" : Movie.objects.get(id = wish_movie),
                }
                UserMovieWish(**wish).save()

    context = {
        'movie_detail': movie_detail,
        'movie_review': movie_review,
        'movie_watch': movie_watch,
    }
    return render(request, "movies/movie_detail.html", context)

