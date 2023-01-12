from scripts.crawler import SeleniumRequest
from scripts.crawler.parser import ottParser, theaterParser
from movies.models import Movie, MovieWatch
from tqdm import tqdm

def run():
    request = SeleniumRequest()

    # OTT -------------------------------------------------------------------
    # 1. movie status = 0 인 영화만 가져오기
    items0 = Movie.objects.filter(status=0)
    print("OTT 서비스 정보 가져오기>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")  

    # 2. title, director 를 검색해서 감상 가능한 곳 crawling
    for item0 in tqdm(items0, 
                        total = len(items0), ## 전체 진행수
                        desc = 'OTT service', ## 진행률 앞쪽 출력 문장
                        ncols = 70, ## 진행률 출력 폭 조절
                        ascii = ' =', ## 바 모양, 첫 번째 문자는 공백이어야 작동
                        leave = True, ## True 반복문 완료시 진행률 출력 남김. False 남기지 않음.
                        ):

        ott_service = request.get("https://pedia.watcha.com/ko-KR", item0.title, item0.director ,callback=ottParser)

        MovieWatch(movie_id=Movie.objects.get(id=item0.id), **ott_service).save()

    # Theater ---------------------------------------------------------------
    # 1. movie status = 1 인 영화만 가져오기
    items1 = Movie.objects.filter(status=1)
    print("현재 상영하는 영화관 정보 가져오기>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    # 2. crawling
    for item1 in tqdm(items1, 
                        total = len(items1), ## 전체 진행수
                        desc = 'theater', ## 진행률 앞쪽 출력 문장
                        ncols = 70, ## 진행률 출력 폭 조절
                        ascii = ' =', ## 바 모양, 첫 번째 문자는 공백이어야 작동
                        leave = True, ## True 반복문 완료시 진행률 출력 남김. False 남기지 않음.
                        ):

        url = f"https://movie.naver.com/movie/bi/mi/running.naver?code={item1.id}"
        theaters = request.get(url, callback=theaterParser)
        
        MovieWatch(movie_id=Movie.objects.get(id=item1.id), **theaters).save()


