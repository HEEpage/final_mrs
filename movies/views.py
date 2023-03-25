from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from django.views.generic import DetailView, ListView

from movies.models import Movie, MovieBoxOffice, MovieUpcoming, MovieWatch, MovieReviewDummy, MovieGenre
from users.models import User, UserMovieWish

from static.models.img_model.utils.evaluate import getImage

# from movies.recommend_movie import recommendation


# 영화 장르 필터링 및 정렬
class MovieGenreList(ListView) :
    template_name = "movies/movie_list.html"

    paginate_by = 20
    paginate_orphans = 3
    
    def get_queryset(self) :
        self.genre = get_object_or_404(MovieGenre, no = self.kwargs["genre_num"])

        return  Movie.objects.filter(genre__contains = self.genre.type).order_by("-avg_grade")  

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["genre"] = self.genre #.type

        page = context["page_obj"]
        paginator = page.paginator
        page_list = paginator.get_elided_page_range(page.number, on_each_side = 3, on_ends = 0)
        context["page_list"] = page_list

        genre_list = MovieGenre.objects.all()
        length = len(genre_list)//2 + 1

        context["genre_type1"] = genre_list[:length]
        context["genre_type2"] = genre_list[length:]

        return context


# 영화 검색
class MovieSearchList(ListView) :
    template_name = "movies/search_list.html"
    paginate_by = 12
    
    def get_queryset(self) :
        keyword = self.request.GET.get('keyword')

        return Movie.objects.filter(
                    Q(title__icontains = keyword) | Q(director__icontains = keyword) | Q(cast__icontains = keyword)
                ).distinct()
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.request.GET.get('keyword')
        context['count'] = Movie.objects.filter(
                    Q(title__icontains= context['keyword'] ) | Q(director__icontains = context['keyword']) | Q(cast__icontains = context['keyword'])
                ).distinct().count()

        genre_list = MovieGenre.objects.all()
        length = len(genre_list)//2 + 1

        context["genre_type1"] = genre_list[:length]
        context["genre_type2"] = genre_list[length:]

        return context


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

    image_ids = getImage(movie_id)
    sim_image = Movie.objects.filter(id__in = image_ids)

    context = {
        'movie_detail': movie_detail,
        'movie_review': movie_review,
        'movie_watch': movie_watch,
        'sim_image': sim_image,
    }

    genre_list = MovieGenre.objects.all()
    length = len(genre_list)//2 + 1

    context["genre_type1"] = genre_list[:length]
    context["genre_type2"] = genre_list[length:]

    return render(request, "movies/movie_detail.html", context)

# def return_recom(request):
    
#     recomm_list = recommendation()

#     for i in range(len(recomm_list)) :
#         recomm_list[f'movie_{i}']['query'] = Movie.objects.filter(id__in = recomm_list[f'movie_{i}']['id'])
    
#     context = {
#         "recomm_list" : recomm_list,
#     }

#     return render(request, "movies/recommendation.html", context)