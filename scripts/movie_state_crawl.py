from scripts.crawler import SeleniumRequest
from scripts.crawler.parser import infoParser, topidParser
from movies.models import Movie, MovieReviewDummy

def run():
    request = SeleniumRequest()

    targets = {
        # 현재 상영 영화
        "current" : {
            "url" : "https://movie.naver.com/movie/running/current.naver",
            "status" : 1,
        },

        # 상영 예정작
        "upcoming" : {
            "url" : "https://movie.naver.com/movie/running/premovie.naver",
            "status" : 2,
        }
    }

    for target in targets.keys():
        # 1. url 요청
        url = targets[target]["url"]
        ids = request.get(url, callback=topidParser)

        print(">>>> " ,len(ids))

        # 현재 Movie 테이블에 status에 해당되는 id 가져오기
        update_status  = Movie.objects.filter(status=targets[target]["status"]).values('id')
        update_lst = [ i['id'] for i in update_status ]
        print("변경 항목 >>>>>>>>>>>>>" , update_lst)


        # 2. movie info 가져오기
        for movie_id in ids:
            print(">>>>>>>>>> " + movie_id + " 정보 가져오는 중 <<<<<<<<<<")

            if movie_id in update_lst:
                update_lst.remove(movie_id)
                continue

            url = f"https://movie.naver.com/movie/bi/mi/point.naver?code={movie_id}"

            if request.get(url, callback= infoParser) is not None:
                movie_info, movie_review = request.get(url, callback= infoParser)

                if target == "current":
                    
                    # 현재상영작 중 Movie에 없는 정보 저장
                    if(Movie.objects.filter(id__iexact=movie_id).count()==0) :
                        Movie(id=movie_id, **movie_info, status = targets[target]["status"]).save()
                        print("===================> 새로운 영화 DB저장 완료, 현재 상영 영화")

                        no = MovieReviewDummy.objects.last().no + 1
                        for review in movie_review:
                            MovieReviewDummy(no=no, movie_id=Movie.objects.get(id=movie_id), grade=review[0], review=review[1], c_date=review[2]).save()
                            no += 1
                    else:
                        # DB에 해당하는 id값이 있으면 status=1로 변경
                        item = Movie.objects.get(id=movie_id)
                        item.status = targets[target]["status"]
                        item.save()
                        print("===================> 현재 상영 영화로 상태 변경", item.title)

                elif target == "upcoming":

                    # 개봉 예정작 중 Movie에 없는 정보 저장
                    if(Movie.objects.filter(id__iexact=movie_id).count()==0) :
                        Movie(id=movie_id, **movie_info, status = targets[target]["status"]).save()
                        print("===================> 새로운 영화 DB저장 완료, 개봉 예정 영화")

                        no = MovieReviewDummy.objects.last().no + 1
                        for review in movie_review:
                            MovieReviewDummy(no=no, movie_id=Movie.objects.get(id=movie_id), grade=review[0], review=review[1], c_date=review[2]).save()
                            no += 1
                    else:
                        # DB에 해당하는 id값이 있으면 status=2로 변경
                        item = Movie.objects.get(id=movie_id)
                        item.status = targets[target]["status"]
                        item.save()
                        print("===================> 개봉 예정작으로 상태 변경", item.title)

        # 상태 변경
        for i in update_lst:
            item = Movie.objects.get(id=i)
            item.status = targets[target]["status"] - 1
            item.save()
            print("===================> 현재 -> 상영끝 / 개봉예정 -> 현재상영 상태 변경", item.title)

