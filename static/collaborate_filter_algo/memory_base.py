import pandas as pd
import numpy as np 
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity

# 모든 영화의 (movie_id) 가중평균 rating을 계산하는 함수

def get_similarity(user_id, movie_id, user_similarity , rating_matrix):
    # 모든 user의 rating 평균
    rating_mean_tb = rating_matrix.mean(axis=1)
    user_rating_mean = rating_mean_tb[user_id]

    if movie_id in rating_matrix:   # 해당 movie_id 존재 확인
    
        # 현재 사용자와 다른 사용자 간의 similarity 가져오기
        sim_scores = user_similarity[user_id]
        
        # 현재 영화에 대한 모든 사용자의 rating값 가져오기
        movie_ratings = rating_matrix[movie_id]
    
        # 해당 item에 대한 rating이 없는 user 삭제
        none_rating_idx = movie_ratings[movie_ratings.isnull()].index
        movie_ratings = movie_ratings.drop(none_rating_idx)
        sim_scores = sim_scores.drop(none_rating_idx)
        rating_mean = rating_mean_tb.drop(none_rating_idx)
        
        # 평균으로부터의 편차 예측치 계산
        movie_ratings = movie_ratings - rating_mean
        prediction = np.dot(sim_scores, movie_ratings) / sim_scores.sum()
        
        # 편차 예측치에 해당 user의 평균 더하기
        prediction = prediction + user_rating_mean

    else:
        #해당 영화가 없으면 해당 사용자의 평균 평점으로 예측 
        prediction = user_rating_mean 
    return prediction

# score 함수 
# def get_score(x_test , user_similarity ,rating_matrix ):
#     ids = zip(x_test['u_id'], x_test['i_id'])
#     y = np.array(x_test['rating'])
#     y_pred = np.array([get_similarity(user, movie , user_similarity ,rating_matrix ) for (user, movie) in ids])
#     return np.sqrt(np.mean((np.array(y) - np.array(y_pred))**2))


# 추천하기
def recommendation (user, movie,  similarity_matrix , rating_matrix , n_items=10):

    # 현재 사용자의 모든 아이템에 대한 예상 평점 계산
    predictions = []
    # 이미 평가한 영화의 인덱스 추출 -> 추천 시 제외해야 함 
    watched = rating_matrix.loc[user][rating_matrix.loc[user].notnull()].index
    # 해당 사용자가 평가하지 않은 영화만 선택 
    items = rating_matrix.loc[user].drop(watched)
    
    # 보지 않은 영화 중, 예상평점 계산
    for item in items.index:
        predictions.append(get_similarity(user, item , similarity_matrix, rating_matrix))

    recommendations = pd.Series(data=predictions, index=items.index, dtype=float)
    recommendations = recommendations.sort_values(ascending=False)[:n_items]        
    recom_items = movie.loc[recommendations.index][['title','genres']]
    return recom_items.index




def memory_main (  user_info , user_data , movie_data ):
    def convert_id(user_info , user_data ):
        id_dictionary = {email : i for i,email in enumerate(user_data["user_email"].unique())}
        # 유저 이메일 id로 변환
        user_data["user_email"] = user_data["user_email"].apply(lambda x :id_dictionary[x] )
        user_data = user_data.rename(columns={'user_email':'userId',"movie_id":'movieId',"grade":"rating"})
        
        user_info["email"] = user_data["email"].apply(lambda x :id_dictionary[x] )
        user_info = user_info.rename(columns={'email':'userId'})
        return user_info , user_data
        
    user_info , user_data = convert_id(user_info , user_data)
    user_id = user_info["userId"]

    full_rating_matrix = user_data.pivot_table(values='rating', index='u_id', columns='i_id')
    full_movies = movie_data[['id', 'title',"genre"]].set_index('id')
    # full_movies = full_movies.set_index('id')
    full_matrix_dummy = full_rating_matrix.copy().fillna(0)
    full_user_similarity = cosine_similarity(full_matrix_dummy, full_matrix_dummy)
    full_user_similarity = pd.DataFrame(full_user_similarity, index=full_rating_matrix.index, columns=full_rating_matrix.index)

    # x_train, x_test= train_test_split(user_data, test_size=0.33, stratify=user_data['u_id'], random_state=42)
    # rating_matrix = x_train.pivot_table(values='rating', index='u_id', columns='i_id')
    # dummy = rating_matrix.copy().fillna(0) 
    # user_similarity = pd.DataFrame(cosine_similarity(dummy, dummy), index=rating_matrix.index, columns=rating_matrix.index)

    # 정확도
    # score = get_score(x_test , user_similarity , rating_matrix)
    # print(score)

    # 모든 사용자의 개별 평점 평균 계산 -  bias from mean average 방식 사용 
    recom_lst = recommendation(user_id, movie_data , full_user_similarity ,full_rating_matrix, 12)
    return recom_lst