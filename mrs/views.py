from django.shortcuts import render
from movies.models import MovieBoxOffice, MovieUpcoming, MovieGenre, Movie
# from movies.recommend_movie_modify import recommendation
import json, os, random

from static.models.user_recom import RecomList

def home(request) :

    # 박스오피스, 개봉예정작 목록
    up_list = MovieUpcoming.objects.all()
    box_list = MovieBoxOffice.objects.all()

    # 관리자 영화 추천 목록 --------------------------------------------------------------------------
    # recomm_list = recommendation()

    # json 파일 경로 만들기
    info_path = '\static\data\host_recomm_list.json'
    json_file = os.getcwd() + info_path

    # json 파일 로드
    with open(json_file, "r", encoding="UTF-8") as f:
        recomm_list = json.load(f)
    
    choice = random.sample(recomm_list.keys() , 4)

    choice_dict = {}
    for mList in choice:
        recomm_list[mList]['query'] = Movie.objects.filter(id__in = recomm_list[mList]["id"])
        choice_dict[mList] = recomm_list[mList]

    # --------------------------------------------------------------------------------------------------
    
    # 개인화된 추천 목록 ----------------------------------------------------------------------------------
    cur_user = request.user

    input_movie = None
    personal = []
    personal_img = []
    if cur_user.is_authenticated:
        login_user = request.user.email


        user = RecomList(login_user)

        # content or collabo
        personal = user.recomUserLogBased()
        personal = Movie.objects.filter(id__in = personal)

        # image
        input_id, personal_img = user.recomImage()
        if input_id is None:
            input_movie = None
            personal_img = []
        else:
            input_movie = Movie.objects.get(id = input_id).title
            personal_img = Movie.objects.filter(id__in = personal_img)

    # --------------------------------------------------------------------------------------------------


    context = {
        "up_list": up_list,
        "box_list": box_list,
        "recomm_list" : choice_dict,
        "personal" : personal,
        "input_movie" : input_movie,
        "personal_img": personal_img,
    }

    genre_list = MovieGenre.objects.all()
    length = len(genre_list)//2 + 1

    context["genre_type1"] = genre_list[:length]
    context["genre_type2"] = genre_list[length:]

    return render(request, "index.html", context)