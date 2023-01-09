from scripts.crawler import SeleniumRequest
from scripts.crawler.parser import top10Parser
from movies.models import MovieBoxOffice, MovieUpcoming, Movie

def run():

    request = SeleniumRequest()
    url = "https://movie.naver.com/"

    # 현재 상영작 top 10
    boxoffice_ids = request.get(url, "boxoffice", callback=top10Parser)

    b_no = 1
    for box_id in boxoffice_ids:

        try:
            MovieBoxOffice(no = b_no, movie_id = Movie.objects.get(id=box_id)).save()
            b_no += 1
        except Exception as e:
            continue

    # 상영 예정작 top 10
    upcoming_ids = request.get(url, "upcoming", callback=top10Parser)

    u_no = 1
    for upcom_id in upcoming_ids:
 
        try:
            # store
            MovieUpcoming(no = u_no, movie_id = Movie.objects.get(id=upcom_id)).save()
            u_no += 1
        except Exception as e:
            continue
