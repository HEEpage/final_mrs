from scripts.crawler import SeleniumRequest
from scripts.crawler.parser import idParser, info_parser

def run():
    request = SeleniumRequest()

    # years = [ 2019, 2020, 2021, 2022, 2023 ]
    years = [ 2022 ]
    datas = {}
    for year in years:
        print(f">>>>>>>>>> {year} 영화 id 가져오는 중 <<<<<<<<<<")
        url = f"https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={year}"
    
        data = request.get( url, callback = idParser )
        
        datas[year] = data

    print(datas)


    # 영화 정보 가져오기
    for movie_id in datas[2022]:
        print(">>>>>>>>>> " + movie_id + " 정보 가져오는 중 <<<<<<<<<<")

        url = f"https://movie.naver.com/movie/bi/mi/point.naver?code={movie_id}"

        if request.get(url, callback= info_parser) is not None:
            movie_info, movie_review = request.get(url, callback= info_parser)

            print(movie_info)
