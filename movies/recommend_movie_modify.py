import random
import pandas as pd 
import numpy as np
from movies.models import Movie, MoviePoint 
from sklearn.metrics.pairwise import cosine_similarity
import scipy as sp
import json

# 공포영화 마니아라면 꼭 봐야 할 영화 
def get_horror(data):
    return {
        "id":list(map(int,data.loc[  (data["fear"]>3)  & (data["tension"]>1)  ].sort_values('weighted_vote',ascending = False)["movie_id_id"])),
        "recom_title":"공포영화 마니아라면 꼭 봐야 할 영화"
    }

# 밤새도록 해 뜰 떄 까지
def enjoy_night(data):
    return {
        "id":list(map(int,data.loc[   (data["immerse"]>4) & (data["direction"]>2) & ((data["tension"] > 2) | (data['story']>3)) ].sort_values('weighted_vote',ascending = False)["movie_id_id"])),
        "recom_title":"밤새도록 해 뜰 때 까지"
    }

# 명품배우 명품연기
def good_acting(data):
    return {
        "id":list(map(int,data.loc[  (data["acting"]>4)  & (data["direction"]>2) & (data["immerse"]>4) ].sort_values('weighted_vote',ascending = False)["movie_id_id"])),
        "recom_title":"명품배우 명품연기"
    }

#2022 한 해를 빛낸 작품
def best_2022(movie_data):
    movie_data["release_year"] = movie_data["release_date"].apply(lambda x : str(x)[:4])
    movie_2022 = movie_data[movie_data["release_year"]=="2022"]
    return {
        "id":list(map(int,movie_2022.sort_values(by=['weighted_vote'], ascending = False).iloc[:10]["movie_id_id"])),
        "recom_title":"2022년 한 해를 빛낸 작품"
    }
def best_2021(movie_data):
    movie_data["release_year"] = movie_data["release_date"].apply(lambda x : str(x)[:4])
    movie_2021 = movie_data[movie_data["release_year"]=="2021"]
    return {
        "id":list(map(int,movie_2021.sort_values(by=['weighted_vote'], ascending = False).iloc[:10]["movie_id_id"])),
        "recom_title":"2021년 한 해를 빛낸 작품"
    }

# 음악을 사랑하는 사람이라면 꼭 봐야할 영화
def music_lover(data):
    return {
        "id":list(map(int,data.loc[  (data["ost"] >4) ].sort_values('weighted_vote',ascending = False)["movie_id_id"])),
        "recom_title":"음악을 사랑하는 사람이라면 꼭 봐야할 영화"
    }

#######################################################################
# 당신이 사랑할 < 로맨스 드라마  , 액션 , 다큐멘터리 ,,, ,,,,, > 

# def romance(data):
#     return {
#         "movie_ids":list(data.loc[(data["멜로/로맨스"] == 1.0 )].sort_values("viewer",ascending =False).iloc[:10]["movie_id_id"]),
#         "recom_title":"당신이 사랑할 < 로맨스 드라마 >"
#     }

#######################################################################
# <내가 본 영화> 과/와 비슷한 콘텐츠
# 영화는 유저 시청 기록 & 평점 좋은 영화 1개 랜덤 반환 
def sim_movie(data):
    movie_id = 10526 
    movie_title = "(임시) 당신이 본 영화 "
    # input,,, 넣어야 해,,, ( 유저 기록에서 랜덤 영화 아이디 반환)  
    # 여기서 data 유저 로그임,, ,,,  
    piv = data.pivot_table(index=['user_email'], columns=['movie_id'], values='grade')
    piv_norm = piv.apply( lambda x: (x-np.mean(x))/(np.max(x)-np.min(x)), axis=1 )
    piv_norm.fillna(0, inplace=True)
    piv_norm = piv_norm.transpose()
    i_sim = cosine_similarity(sp.sparse.csr_matrix(piv_norm.values))
    item_sim_df = pd.DataFrame(i_sim, piv_norm.index, piv_norm.index)
    return {
        "id":list(map(int, item_sim_df.loc[~item_sim_df.index.isin([movie_id]), movie_id].sort_values(ascending = False)[:10])),
        "recom_title":f"<{movie_title}> 와 비슷한 영화"
    }

#######################################################################
# 짜릿한 액션 영화
def good_action(data):
    return {
        "id":list(map(int,data.loc[  (data["immerse"]>3.5)  & (data["acting"]>2) & (data["액션"] == 1.0 )  ].sort_values('weighted_vote',ascending = False)["movie_id_id"])),
        "recom_title":"짜릿한 액션 영화"
    }

# 가슴 절절한 로맨스 영화
def sad_romance(data):
    return {
        "id":list(map(int,data.loc[ (data["immerse"]>3)  & (data["acting"]>2) 
        & (data["멜로/로맨스"] == 1.0 )  ].sort_values('weighted_vote',ascending = False)  ["movie_id_id"])),
        "recom_title":"가슴 절절한 로맨스 영화"
    }



def countVec( df , col ):
    str_connector = "|"
    all_cols = [ x.split(str_connector)[i] for x in df[col] for i in range(len(x.split(str_connector)))   ]
    uniq_col_lst = pd.unique( sorted( all_cols ) ) 
    # create dummy DF
    zero_metrix = np.zeros((len(df[col]), len(uniq_col_lst)))
    dummy = pd.DataFrame(zero_metrix, columns=uniq_col_lst)
    # count genres
    for i, gen in enumerate(df[col]):
        indices = dummy.columns.get_indexer(  gen.split(str_connector) )
        dummy.iloc[i, indices] = 1

    return dummy



def recommendation():
    movie_detail = pd.DataFrame(list(Movie.objects.all().values())) 
    movie_point = pd.DataFrame(list(MoviePoint.objects.all().values()))

    # 장르 카운터 벡터라이즈 & 머지
    movie_detail = pd.concat([movie_detail,countVec(movie_detail,"genre")],axis = 1).drop(columns = "genre")
    result_set = pd.merge( movie_detail , movie_point, how = "left", left_on="id", right_on="movie_id_id" )

    # 가중치 점수 추가 
    m = result_set['viewer'].quantile(0.99 ) # 높아질수록, 투표 횟수가 많은 영화에 더 많은 가중치
    def get_weighted_score( record ):
            v = record.loc['viewer']
            R = record.loc['avg_grade']
            return (v*R)/(v+m)

    result_set["weighted_vote"] = result_set.apply(lambda x : get_weighted_score(x), axis = 1)

    # 생성한 함수 명 적어두기 
    func_lst = [get_horror , enjoy_night,good_acting,best_2021, music_lover,best_2022,good_action , sad_romance    ]

    ###################################### 기연 추가 ######################################################
    # 불러오는데 시간이 오래걸려서 json 파일로 저장해서 가져오는 형태로 할까 생각함
    total_lst = {}
    for i in range(len(func_lst)):
        total_lst[f'movie_{i}'] = func_lst[i](result_set)

    # 저장하기
    with open(f'./static/data/host_recomm_list.json', 'w', encoding="utf-8") as f:
        json.dump(total_lst, f, ensure_ascii=False, indent=4)
    ######################################################################################################

    choice = random.sample(func_lst , 4) # 랜덤으로 함수 4개 선택
    return_lst = {}

    for i in range(len(choice)):
        return_lst[f'movie_{i}'] = choice[i](result_set)

    return return_lst



