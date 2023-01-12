import os, json
from movies.models import Movie, MovieReviewDummy
from tqdm import tqdm

def run() :

    Movie.objects.all().delete()

    # data store ------------------------------------------
    
    years = [ 2019, 2020, 2021, 2022, 2023 ]
    no = 1

    for year in tqdm(years, 
                        total = len(years), ## 전체 진행수
                        desc = 'DATA STORE', ## 진행률 앞쪽 출력 문장
                        ncols = 70, ## 진행률 출력 폭 조절
                        ascii = ' =', ## 바 모양, 첫 번째 문자는 공백이어야 작동
                        leave = True, ## True 반복문 완료시 진행률 출력 남김. False 남기지 않음.
                        ):

        # json 파일 경로 만들기
        info_path = f'\static\data\{year}_movie_info.json'
        json_file = os.getcwd() + info_path

        # json 파일 로드
        with open(json_file, "r", encoding="UTF-8") as f:
            movie_info = json.load(f)

        for id, info in movie_info.items() :
            # DB에 해당 id 값이 없으면 저장
            if(Movie.objects.filter(id__iexact=id).count()==0) :
                Movie(id=id, **info).save()


        # json 파일 경로 만들기
        review_path = f'\static\data\{year}_movie_review.json'
        json_file = os.getcwd() + review_path

        # json 파일 로드
        with open(json_file, "r", encoding="UTF-8") as f:
            movie_review = json.load(f)

        for m_id, reviews in movie_review.items():
            for review in reviews:
                MovieReviewDummy(no=no, movie_id=Movie.objects.get(id=m_id), **review).save()
                no += 1