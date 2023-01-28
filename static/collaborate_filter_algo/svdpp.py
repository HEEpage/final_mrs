import numpy as np
import pandas as pd
import numpy as np
import pandas as pd
import pickle
import joblib
import surprise
from surprise import Dataset ,Reader,SVD, SVDpp, SlopeOne, NMF, NormalPredictor, KNNBasic, KNNBaseline, KNNWithMeans, KNNWithZScore, BaselineOnly, CoClustering
from surprise.model_selection import cross_validate , train_test_split
from surprise import accuracy


def recommendation(algo, user_id , user_data , movie_data, top_n = 100):
    def get_new_mv (user_id ,user_data, movie_data):
        watched_mv = user_data[user_data["userId"] == user_id ]["movieId"].tolist()
        total_mv = movie_data['id'].tolist()
        not_watched = [ mv for mv in total_mv if mv not in watched_mv ]
        # print(f"{user_id}번 유저가 본 영화수 : { len(watched_mv)} \n 안본 영화 개수 : {len(notwatched)}\n 전체영화수:{len(total_mv)}")
        return not_watched

    def sortkey_est(pred):
        return pred.est

    not_watched = get_new_mv (user_id ,user_data, movie_data)

    predictions = [algo.predict(user_id, mv_id) for mv_id in not_watched ]
    # print(predictions)
    predictions.sort(key=sortkey_est , reverse = True)
    top_predictions = predictions[:top_n]

    top_mvs = [ int(pred.iid) for pred in top_predictions ]
    top_ratings = [ pred.est for pred in top_predictions]
    top_title = movie_data[movie_data.id.isin(top_mvs)]["title"]

    pred = [ (ids, rating, title) for ids, rating, title in zip(top_mvs, top_ratings,top_title)]
    return pred

def run(  user_info , user_data , movie_data ):
    
    def convert_id(user_info , user_data ):
        id_dictionary = {email : i for i,email in enumerate(user_data["user_email"].unique())}
        # 유저 이메일 id로 변환
        user_data["user_email"] = user_data["user_email"].apply(lambda x :id_dictionary[x] )
        user_data = user_data.rename(columns={'user_email':'userId',"movie_id":'movieId',"grade":"rating"})
        
        user_info["email"] = user_data["email"].apply(lambda x :id_dictionary[x] )
        user_info = user_info.rename(columns={'email':'userId'})
        return user_info , user_data
        
    user_info , user_data = convert_id(user_info , user_data)
    reader = Reader(rating_scale=( user_data["rating"].min()   ,  user_data["rating"].max()    ))

    user_id = user_info["userId"]

    data = Dataset.load_from_df(user_data[['userId', 'movieId', 'rating']], reader=reader)

    trainset, testset = train_test_split(data, test_size=.33, random_state=42)

    # pickle file code 
    # fold = 5
    # algo = SVDpp(n_factors=40, n_epochs=40, lr_all=0.008, reg_all=0.1)
    # cross_validate(algo,data, measures=['RMSE', 'MAE'], cv=fold, verbose=True)
    # #Train the Model
    # model = SVDpp(n_factors=40, n_epochs=10, lr_all=0.008, reg_all=0.1)
    # model.fit(trainset)
    # # 파일 저장
    # joblib.dump(model, f'{PATH}DATA/l_crawl_svdplus_model.pkl')

    model = joblib.load('l_crawl_svdplus_model.pkl')
    #validate the model
    pred = model.test(testset)
    # print("::: crawl  RMSE SVD++ results ::: ")
    # accuracy.rmse(pred, verbose=True)

    trainset, testset = train_test_split(data, test_size=.2)
    algo = SVDpp(n_factors=50, n_epochs=20 , random_state = 42)
    algo.fit(trainset)

    top_preds = recommendation(algo, user_id , user_data, movie_data , top_n = 12)

    # print("##### 추천 리스트 #### ")
    # for top in top_preds:
    #     print("ID: (",top[0],") , title : ",top[2])
    #     print("pred_Score : ",top[1])
    recom_lst = [top[0] for top in top_preds ]
    return recom_lst


