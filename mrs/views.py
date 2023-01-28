from django.shortcuts import render
from movies.models import MovieBoxOffice, MovieUpcoming, MovieGenre, Movie
# from movies.recommend_movie_modify import recommendation
import json, os, random

from static.model.user_recom import getRecomList

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

    test_lst = []
    if cur_user.is_authenticated:
        login_user = request.user.email


        test_lst = getRecomList(login_user)
        test_lst = Movie.objects.filter(id__in = test_lst)
    
    context = {
        "up_list": up_list,
        "box_list": box_list,
        "recomm_list" : choice_dict,
        "test_lst" : test_lst,
    }

    genre_list = MovieGenre.objects.all()
    length = len(genre_list)//2 + 1

    context["genre_type1"] = genre_list[:length]
    context["genre_type2"] = genre_list[length:]

    return render(request, "index.html", context)