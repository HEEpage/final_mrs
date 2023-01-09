from scripts.crawler import SeleniumRequest
from scripts.crawler.parser import ottParser, theaterParser
from movies.models import Movie, MovieWatch

def run():
    request = SeleniumRequest()

    # OTT -------------------------------------------------------------------
    # 1. movie status = 0 인 영화만 가져오기
    items0 = Movie.objects.filter(status=0)

    # 2. title, director 를 검색해서 감상 가능한 곳 crawling
    for item0 in items0:
        ott_service = request.get("https://pedia.watcha.com/ko-KR", item0.title, item0.director ,callback=ottParser)
        print(ott_service)
    #     MovieWatch(movie_id=Movie.objects.get(id=item0.id), **ott_service).save()

    # Theater ---------------------------------------------------------------
    # 1. movie status = 1 인 영화만 가져오기
    items1 = Movie.objects.filter(status=1)

    # 2. crawling
    for item1 in items1:
        url = f"https://movie.naver.com/movie/bi/mi/running.naver?code={item1.id}"
        theaters = request.get(url, callback=theaterParser)
        print(theaters)
        # MovieWatch(movie_id=Movie.objects.get(id=item1.id), **theaters).save()


