import pandas as pd
import numpy as np
import json
import pickle
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import lightgbm as lgb
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.metrics.pairwise import cosine_similarity
import category_encoders as ce

import pandas as pd
import numpy as np
import category_encoders as ce
from sklearn.preprocessing import LabelEncoder
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import lightgbm as lgb

class CFG :
    SEED = 42

class Enc:
    def binaryEncoding(df , col):
        enc_binary = ce.BinaryEncoder()
        df_binary = enc_binary.fit_transform(df[col])
        return pd.concat([df, df_binary], axis=1)

    def labelEncoding(df , col):
        enc_label = LabelEncoder()
        df[col] = enc_label.fit_transform(df[col])
        return df
    
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

def imute_missingValue( movie_info ):
    #3. 날짜 12월31일로 채우기 
    movie_info["release_date"] = movie_info["release_date"].apply(lambda x : x+'1231' if len(x.split("-"))<2 else ( x+"31" if len(x.split("-"))<3  else  "".join(x.split("-")) ) )
    
    # 1. 문자열 데이터 결측치 채우기 
    col_list_str = [ col for col in movie_info.columns if ( movie_info[col].isnull().sum() >0 and type(movie_info[col].iloc[0]) == type("s"))]
    # 결측치 채우기
    for i in col_list_str:
        movie_info[i] = movie_info[i].fillna(  "정보없음" )

    #2. numeric value - IterativeImputer로 채우기 
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
    cols = ['poster']
    movie_info = movie_info.drop(columns = cols)

    # 결측치 채우기 
    movie_info = imute_missingValue(   movie_info  )

    # 나라 수정 (한국, 미국만 남기기)
    for idx, x in enumerate(movie_info["nation"]):
        result = [ i for i in x.split("|") if i in ["대한민국","미국"] ]
        movie_info["nation"].iloc[idx] = "|".join(sorted(result))

    percent = 0.8  
    m = movie_info['viewer'].quantile(percent) # 높아질수록, 투표 회수가 많은 영화에 더 많은 가중치 
    C = movie_info['avg_grade'].mean()

    def get_weighted_score( record ):
        v = record['viewer']
        R = record['avg_grade']
        return (v*R + m*C)/(v+m)

    movie_info["weighted_vote"] = movie_info.apply(get_weighted_score, axis = 1)

    # 영화 등급 - 라벨인코딩
    movie_info = Enc.labelEncoding(movie_info, "ratings")  

    # 장르 - 카운드 벡터
    movie_info = pd.concat([movie_info, Enc.countVec(movie_info, "genre")  ], axis=1)
    dummy= Enc.countVec(movie_info, "genre") 

    # 감독 - 바이너리 
    movie_info = Enc.binaryEncoding(movie_info, "director") 

    # 국가 - 바이너리 
    movie_info = Enc.binaryEncoding(movie_info, "nation")

    drop_cols = ["synopsis" , 'status',"nation","genre","director","keyword",'cnt_click','running_time']
    movie_info = movie_info.drop(columns = drop_cols)
    
    return movie_info , dummy

def find_movie( movie_info , genre_dummy , index ,top_n=20 ):

    genre_sim = cosine_similarity(genre_dummy , genre_dummy)
    sorted_genre_sim = genre_sim.argsort()[:,::-1]
    sim_idx = sorted_genre_sim[index, : top_n].reshape(-1)

    return movie_info.iloc[sim_idx][["id",'title']].iloc[1:]['id'].values
    
def prefer_movie_reco (  user , movie_info ):
    recommend = []
    preference = user["preference_genre"].values[0].split(",")

    for idx in range(len(preference)):
        cols = ["id","title","weighted_vote"]
        recommend.append(movie_info[movie_info[preference[idx]] > 0.2 ][cols].sort_values(by = ["weighted_vote"] , ascending = False)[:10]["id"].values )
    new_lst = np.array(recommend[0])
    for i in range(1,len(preference)):
        new_lst = np.concatenate((new_lst,recommend[i]) , axis = 0)

    if len(new_lst)<12:
        return new_lst[np.random.choice(range(0, len(new_lst)), len(new_lst)-1 , replace = False)]
    else:
        return new_lst[np.random.choice(range(0, len(new_lst)), 12 , replace = False)]

def main(  user_info , input_user_log , movie_info ):
    movie_info , genre_dummy = movieInfo_preprocessing ( movie_info )

    # 유저 기록 없는 사용자 
    if input_user_log.empty:
        return prefer_movie_reco (  user_info , movie_info)

    movie_id = input_user_log.sort_values(by=['grade'] , ascending= False   )["movie_id"].iloc[0]
    input_idx = movie_info.reset_index()[ movie_info["id"] == movie_id]['index'].values[0]

    # 유저 기록 3개 이하 
    if len(input_user_log) < 4:
        new_lst = np.concatenate((prefer_movie_reco (  user_info , movie_info) , find_movie( movie_info ,genre_dummy,  input_idx)  ) , axis = 0)
        if len(new_lst) < 12:
            return new_lst[np.random.choice(range(0, len(new_lst)), len(new_lst)-1 , replace = False)]
        else:
            return new_lst[np.random.choice(range(0, len(new_lst)), 12 , replace = False)]
    
    # 기타
    else:

        lst = find_movie( movie_info ,genre_dummy,  input_idx)

        if len(lst) < 8:
            return lst
        else:
            return lst[:8]

    



