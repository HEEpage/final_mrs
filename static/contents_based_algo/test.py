import sqlite3
import pandas as pd
from static.contents_based_algo.v1_HN_md import main
# from sum_algo_v2 import run

MOVIE_COL = ['id', 'title', 'poster', 'director', 'cast', 'genre', 'nation', 'running_time', 'release_date', 'ratings', 'synopsis', 'keyword', 'status', 'avg_grade', 'viewer', 'cnt_click']
USER_COL = ['email', 'username', 'gender', 'birth', 'preference_genre']
USER_MOVIE_LOG_COL = ['user_email', 'movie_id', 'grade']

def getRecomList(login_user):
    # 1. db 연결 객체 생성
    conn = sqlite3.connect('C:/final_project/final_mrs/db.sqlite3')

    # 2. cursor 객체 생성
    cur = conn.cursor()

    # 3. sql문 작성 및 출력
    query1 = "SELECT * FROM movies_movie"
    query2 = f"SELECT email, username, gender, birth, preference_genre FROM users_user where email = '{login_user}'"
    query3 = f"SELECT user_email, movie_id, grade FROM users_usermovielog where user_email = '{login_user}'"

    movie_rows = cur.execute(query1)

    movie_df = pd.DataFrame(movie_rows, columns=MOVIE_COL)
    # print(movie_df)

    user_rows = cur.execute(query2)

    user_df = pd.DataFrame(user_rows, columns=USER_COL)
    # print(user_df)

    usermovielog_rows = cur.execute(query3)

    usermovielog_df = pd.DataFrame(usermovielog_rows, columns=USER_MOVIE_LOG_COL)
    # print(usermovielog_df)

    usermovielog_df['user_email'] = usermovielog_df['user_email'].str.split('@').str[0]
    # print(usermovielog_df)

    # v1_HN_md
    recom_ids = main(user_df, usermovielog_df, movie_df)
    
    return recom_ids

    # # sum_algo_v2
    # recom_ids2 = run(user_df, usermovielog_df)
    # print(recom_ids2)

# print(getRecomList("test1@mrs.com"))