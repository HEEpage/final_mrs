import sqlite3
import pandas as pd
import random
from .contents_based_algo.v1_HN_md import main
from .collaborate_filter_algo.svdpp import run
from .img_model.utils.evaluate import getImage

MOVIE_COL = ['id', 'title', 'poster', 'director', 'cast', 'genre', 'nation', 'running_time', 'release_date', 'ratings', 'synopsis', 'keyword', 'status', 'avg_grade', 'viewer', 'cnt_click']
USER_COL = ['email', 'username', 'gender', 'birth', 'preference_genre']
USER_MOVIE_LOG_COL = ['user_email', 'movie_id', 'grade']

class RecomList:
    def __init__(self, login_user):
        self.login_user = login_user

        # 1. db 연결 객체 생성
        self.conn = sqlite3.connect('C:/final_project/final_mrs/db.sqlite3')
        # 2. cursor 객체 생성
        self.cur = self.conn.cursor()

    def getDataFrame(self, query, columns):
        rows = self.cur.execute(query)
        df = pd.DataFrame(rows, columns=columns)
        return df

    def recomUserLogBased(self):

        #sql문 작성 및 출력
        query1 = "SELECT * FROM movies_movie" # 영화 전체 기록
        query2 = f"SELECT email, username, gender, birth, preference_genre FROM users_user where email = '{self.login_user}'" # 유저 개인정보
        query3 = f"SELECT user_email, movie_id, grade FROM users_usermovielog where user_email = '{self.login_user}'" # 개인 기록
        query4 = f"SELECT user_email, movie_id, grade FROM users_usermovielog" # 유저 영화 기록 전체
        

        movie_df = self.getDataFrame(query1, MOVIE_COL)
        user_df = self.getDataFrame(query2, USER_COL)

        usermovielog_df = self.getDataFrame(query3, USER_MOVIE_LOG_COL)
        usermovielog_df['user_email'] = usermovielog_df['user_email'].str.split('@').str[0]

        user_all_df = self.getDataFrame(query4, USER_MOVIE_LOG_COL)
        

        # content based / collabo based
        if len(usermovielog_df) < 10 or usermovielog_df is None:
            recom_ids = main(user_df, usermovielog_df, movie_df)
        
        else:
            # svdpp
            svdpp_ids = run(user_df, user_all_df, movie_df)

            if len(svdpp_ids) > 8:
                recom_ids = random.sample(svdpp_ids,8) 
            else:
                recom_ids = svdpp_ids

        return recom_ids

    def recomImage(self):

        query5 = f"SELECT user_email, movie_id, grade FROM users_usermovielog where user_email = '{self.login_user}' order by grade DESC limit 3" # 개인 기록 상위 3개

        user_top3_df = self.getDataFrame(query5, USER_MOVIE_LOG_COL)

        input_id = None
        image_ids = []
        # image similarity
        if not user_top3_df.empty:
            top3_ids = user_top3_df["movie_id"].tolist()
            input_id = random.choice(top3_ids)
            image_ids = getImage(input_id)

        return input_id, image_ids

