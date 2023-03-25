from scripts.crawler import SeleniumRequest
from scripts.crawler.parser import idParser, infoParser

import os
from urllib.request import urlretrieve
from PIL import Image

from movies.models import Movie, MovieReviewDummy
import json

def run():
    
    #이미지 저장할 폴더 경로 
    # img_folder_path = './static/imgs'

    MovieReviewDummy.objects.all().delete()
    Movie.objects.all().delete()

    request = SeleniumRequest()


    # 연도별 id 가져오기
    years = [ 2019, 2020, 2021, 2022, 2023 ]

    m_ids = {}
    for year in years:
        print(f">>>>>>>>>> {year} 영화 id 가져오는 중 <<<<<<<<<<")
        url = f"https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={year}"
        print(url)
    
        data = request.get( url, callback = idParser )

        m_ids[year] = data

    
    # 영화 정보 가져오기
    for y, movie_ids in m_ids.items():

        print(f">>>>>>>>>>>>>>{y}<<<<<<<<<<<<<<<<<<<<<<<<")
        movies = {}
        reviews = {}

        for movie_id in movie_ids:
            print(">>>>>>>>>> " + movie_id + " 정보 가져오는 중 <<<<<<<<<<")

            url = f"https://movie.naver.com/movie/bi/mi/point.naver?code={movie_id}"

            if request.get(url, callback= infoParser) is not None:
                movie_info, movie_review = request.get(url, callback= infoParser)

                # 이미지 저장
                # 폴더가 없으면 새로 생성
                # if not os.path.isdir(img_folder_path) :
                #     os.mkdir(img_folder_path)

                # img_path = './static/imgs/{}{}'.format(movie_id, '.png')

                # urlretrieve(movie_info['poster'], img_path)

                # image = Image.open(img_path)
                # image = image.resize((450,600))

                # if image.mode not in ["1", "L", "P", "RGB", "RGBA"]:
                #     image = image.convert("RGB")

                # image.save(img_path)


                # 영화 정보 저장
                if(Movie.objects.filter(id__iexact=movie_id).count()==0) :
                    Movie(id=movie_id, **movie_info).save()

                for review in movie_review:
                    MovieReviewDummy(movie_id=Movie.objects.get(id=movie_id), **review).save()
        
                movies[movie_id] = movie_info
                reviews[movie_id] = movie_review

        # 저장하기
        with open(f'./static/data/{y}_movie_info.json', 'w', encoding="utf-8") as f:
            json.dump(movies, f, ensure_ascii=False, indent=4)

        with open(f'./static/data/{y}_movie_review.json', 'w', encoding="utf-8") as f:
            json.dump(reviews, f, ensure_ascii=False, indent=4)