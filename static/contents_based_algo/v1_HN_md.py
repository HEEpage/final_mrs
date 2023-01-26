import pandas as pd
import numpy as np
import json
import pickle
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder
import lightgbm as lgb
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.metrics.pairwise import cosine_similarity

class CFG :
    SEED = 42

def imute_missingValue( movie_info ):
    # 1. director - "정보없음 "
    movie_info['director'] = movie_info['director'].fillna(  "정보없음" )

    # 2. 최빈값으로 채우기 
    cols = ['ratings']
    for i in cols:
        movie_info[i] = movie_info[i].fillna(   movie_info[i].mode()[0] )
    
    #3. numeric value - IterativeImputer로 채우기 
    # 결측값 있는 리스트 
    col_list_num = [ col for col in movie_info.columns if ( movie_info[col].isnull().sum() >0 and type(movie_info[col].iloc[0]) != type("s"))]
    
    # col_list_num 결측치 채우기
    for i in col_list_num:
        imputer = IterativeImputer(estimator =  lgb.LGBMRegressor(),random_state=CFG.SEED)
        movie_info[i] = imputer.fit_transform(movie_info[[i]])

    return movie_info

def get_dummy( movie_info , target ):
    all_lst = []
    nation_target = "독일(구 서독)"

    for x in movie_info[target]:
        for i in range(len(x.split(","))):
            if x.split(",")[i] ==  nation_target :
                x = x.replace( x.split(",")[i] ,target.split("(")[0] )
            all_lst.append( x.split(",")[i] )
    lst = pd.unique(sorted(all_lst)) # 중복 제거한 국가 리스트
    zero_metrix = np.zeros((len(movie_info[target]), len(lst)))
    dummy = pd.DataFrame(zero_metrix, columns=lst)

    for i, gen in enumerate(movie_info[target]):
        indices = dummy.columns.get_indexer(  gen.split(",") )
        dummy.iloc[i, indices] = 1

    return dummy

def movieInfo_preprocessing ( movie_info ):
    # drop columns
    cols = ['release_date', 'poster'] # title
    # print("movieL: ",movie_info)
    movie_info = movie_info.drop(columns = cols)

    # 결측치 채우기 
    movie_info = imute_missingValue(   movie_info  )

    # add columns 
    # 1. 평점 - IMDB 가중 평점 ( Weighted Rating ) 
    # v : 투표수 , m : 최소 투표수 , R : 개별영화 평균평점 , C : 전체 영화 평균평점 
    # m값 보다 v가 낮으면 개별 평점이 좋더라도 값이 작아짐

    percent = 0.8  
    m = movie_info['viewer'].quantile(percent) # 높아질수록, 투표 회수가 많은 영화에 더 많은 가중치 
    C = movie_info['avg_grade'].mean()

    def get_weighted_score( record ):
        v = record['viewer']
        R = record['avg_grade']
        return (v*R + m*C)/(v+m)

    movie_info["weighted_vote"] = movie_info.apply(get_weighted_score, axis = 1)
    spec_table = movie_info.copy()

    # 2. add dummy (unique values)
    dummy_cols = ["nation","cast","genre"]
    for col in dummy_cols:
        dummy = get_dummy(movie_info,col)
        movie_info = pd.concat([movie_info, dummy ],axis = 1)
        if col != "nation":
            spec_table = pd.concat([spec_table, dummy ],axis = 1)
        if col != "genre":
            movie_info = movie_info.drop(columns = col)

    # 3. onehot encoding 
    def onehotEnc(  df, cols     ):
        enc = OneHotEncoder(handle_unknown='ignore')
        tmp = pd.DataFrame(
            enc.fit_transform(df[cols]).toarray(),
            columns = enc.get_feature_names_out()
        )
        return pd.concat([df, tmp], axis=1).drop(columns = cols)

    movie_info = onehotEnc(  movie_info  ,  ['ratings', 'director' , 'genre' ]     )
    spec_table = onehotEnc(  spec_table  , ['genre' ,'director' ]    )

    # 4. drop_col
    drop_col = ['title',  'nation', 'cast', 'running_time', 'ratings', 'avg_grade', 'viewer',   'status'  ]
    spec_table = spec_table.drop(columns = drop_col)
    return movie_info, spec_table ,dummy

def get_knn(id  , df ): 
    table = df.drop(columns = ["id",'title'])
    target = table.iloc[id-1,: ]
    nbrs = NearestNeighbors(n_neighbors=75).fit(table.values) 
    dist , idx = nbrs.kneighbors([target])
    recomm = df.loc[ idx[0] , ['title']  ]
    recomm['distance'] = dist[0]
    if idx-1 in idx:
        recomm = recomm.drop([idx - 1])
    tmp = recomm.reset_index()["index"]
    return tmp

def find_movie( movie_info , genre_dummy , index ,top_n=20 ):
    movie_lst = [] 
    
    genre_sim = cosine_similarity(genre_dummy , genre_dummy)
    sorted_genre_sim = genre_sim.argsort()[:,::-1]
    sim_idx = sorted_genre_sim[index, : top_n].reshape(-1)

   

    return movie_info.iloc[sim_idx][["id",'title']].iloc[1:]['id'].values
    
def prefer_movie_reco (  user , movie_info ):
    recommend = []
    preference = user["preference_genre"].values[0].split(",")

    for idx in range(len(preference)):
        cols = ["id","title","weighted_vote"]
        recommend.append(movie_info[movie_info["genre_"+preference[idx]] >0.2 ][cols].sort_values(by = ["weighted_vote"] , ascending = False)[:10]["id"].values )
    new_lst = np.array(recommend[0])
    for i in range(1,len(preference)):
        new_lst = np.concatenate((new_lst,recommend[i]) , axis = 0)
    return new_lst[np.random.choice(range(0, len(new_lst)), 5 , replace = False)]

def main(  user_info , input_user_log , movie_info ):
    # input_user_log = pd.DataFrame(input_user_log)
    # movie_info = pd.DataFrame(movie_info)
    movie_info ,spec_table , genre_dummy = movieInfo_preprocessing ( movie_info )

    try:
        movie_id = input_user_log.sort_values(by=['avg_grade'] , ascending= False   )["movie_id"].iloc[0]
        input_idx = movie_info.reset_index()[ movie_info["id"] == movie_id]['index'].values[0] 


        return find_movie( movie_info ,genre_dummy,  input_idx) 


    except : 
        # user = pd.DataFrame(user_info) 
        # prefer genre 기반해서 영화 추천 & 장르별로 탑티어 10개씩 뽑아서 랜덤으로 5개 반환 ?  
        return prefer_movie_reco (  user_info , movie_info)

