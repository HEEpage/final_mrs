from scripts.crawler import SeleniumRequest
from scripts.crawler.parser import idParser, infoParser

# import os
# from urllib.request import urlretrieve
# from PIL import Image

from movies.models import Movie, MovieReviewDummy

def run():
    # Movie.objects.all().delete()

    request = SeleniumRequest()

    # years = [ 2019, 2020, 2021, 2022, 2023 ]
    search = [
        ( 2022, "US"),
        ( 2022, "KR"),
        ( 2023, "US"),
        ( 2023, "KR"),
    ]

    m_ids = []
    # for year in years:
    for year, nation in search:
        print(f">>>>>>>>>> {year} 영화 id 가져오는 중 <<<<<<<<<<")
        url = f"https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={year}&nation={nation}"
        # url = f"https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={year}"
        print(url)
    
        m_id = request.get( url, callback = idParser )
        
        m_ids += m_id

    # 이미지 저장할 폴더 경로 
    # img_folder_path = 'C:/final_project/final_mrs/static/imgs'
    print("--------------------------------------")
    print(len(m_ids))
    print("--------------------------------------")

    no = 0
    # 영화 정보 가져오기
    for movie_id in m_ids:

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
            # image.save(img_path)

            # 영화 정보 저장
            if(Movie.objects.filter(id__iexact=movie_id).count()==0) :
                Movie(id=movie_id, **movie_info).save()


            for review in movie_review:
                MovieReviewDummy(no=no, movie_id=Movie.objects.get(id=movie_id), grade=review[0], review=review[1], c_date=review[2]).save()
                no += 1