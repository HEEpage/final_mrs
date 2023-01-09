from scripts.crawler import SeleniumRequest
from scripts.crawler.parser import idParser, info_parser

# import os
# from urllib.request import urlretrieve
# from PIL import Image

from movies.models import Movie

def run():
    Movie.objects.all().delete()

    request = SeleniumRequest()

    # years = [ 2019, 2020, 2021, 2022, 2023 ]
    years = [ 2022 ]
    datas = {}
    for year in years:
        print(f">>>>>>>>>> {year} 영화 id 가져오는 중 <<<<<<<<<<")
        url = f"https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={year}"
    
        data = request.get( url, callback = idParser )
        
        datas[year] = data


    # 영화 정보 가져오기
    for movie_id in datas[2022]:
        print(">>>>>>>>>> " + movie_id + " 정보 가져오는 중 <<<<<<<<<<")

        url = f"https://movie.naver.com/movie/bi/mi/point.naver?code={movie_id}"

        if request.get(url, callback= info_parser) is not None:
            movie_info, movie_review = request.get(url, callback= info_parser)

            print(movie_info)

            # 영화 정보 저장
            if(Movie.objects.filter(id__iexact=movie_id).count()==0) :
                Movie(id=movie_id, **movie_info).save()
        
