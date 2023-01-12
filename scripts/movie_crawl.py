from scripts.crawler import SeleniumRequest
from scripts.crawler.parser import idParser, infoParser

import os
from urllib.request import urlretrieve
from PIL import Image

from movies.models import Movie, MovieReviewDummy
import json

def run():
    
    #이미지 저장할 폴더 경로 
    img_folder_path = './static/imgs'

    # Movie.objects.all().delete()

    request = SeleniumRequest()

    years = [ 2023 ]
    # search = [
    #     ( 2019, "US"),
    #     ( 2019, "KR"),

    #     ( 2020, "US"),
    #     ( 2020, "KR"),

    #     ( 2021, "US"),
    #     ( 2021, "KR"),

    #     ( 2022, "US"),
    #     ( 2022, "KR"),

    #     ( 2023, "US"),
    #     ( 2023, "KR"),
    # ]

    m_ids = {}
    # for year in years:
    for year in years:

        print(f">>>>>>>>>> {year} 영화 id 가져오는 중 <<<<<<<<<<")
        # url = f"https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={year}&nation={nation}"
        url = f"https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={year}"
        print(url)
    
        data = request.get( url, callback = idParser )

        m_ids[year] = data

   
    print("--------------------------------------")
    print(len(m_ids))
    # print("2019 >>> ", len(m_ids[2019]))
    # print("2020 >>> ", len(m_ids[2020]))
    # print("2021 >>> ", len(m_ids[2021]))
    # print("2022 >>> ", len(m_ids[2022]))
    print("2023 >>> ", len(m_ids[2023]))
    print("--------------------------------------")

    no = 0
    
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
                if not os.path.isdir(img_folder_path) :
                    os.mkdir(img_folder_path)

                img_path = './static/imgs/{}{}'.format(movie_id, '.png')

                urlretrieve(movie_info['poster'], img_path)

                image = Image.open(img_path)
                image = image.resize((450,600))

                if image.mode not in ["1", "L", "P", "RGB", "RGBA"]:
                    image = image.convert("RGB")

                image.save(img_path)

                movies[movie_id] = movie_info
                reviews[movie_id] = movie_review

        # 저장하기
        with open(f'./static/data/{y}_movie_info.json', 'w', encoding="utf-8") as f:
            json.dump(movies, f, ensure_ascii=False, indent=4)

        with open(f'./static/data/{y}_movie_review.json', 'w', encoding="utf-8") as f:
            json.dump(reviews, f, ensure_ascii=False, indent=4)

        print(len(movies))
        print(len(reviews))

                # 영화 정보 저장
                # if(Movie.objects.filter(id__iexact=movie_id).count()==0) :
                #     Movie(id=movie_id, **movie_info).save()


                # for review in movie_review:
                #     MovieReviewDummy(no=no, movie_id=Movie.objects.get(id=movie_id), grade=review[0], review=review[1], c_date=review[2]).save()
                #     no += 1