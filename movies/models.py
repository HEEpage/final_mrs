from django.db import models

# 영화 정보 테이블
class Movie(models.Model) :
    
    id = models.IntegerField(primary_key=True) # 영화 고유 ID

    title = models.CharField(max_length=100) # 제목
    poster = models.CharField(max_length=100, blank=True) # 포스터 이미지 url

    director = models.CharField(max_length=50, blank=True) # 감독
    cast = models.CharField(max_length=200, blank=True) # 출연진

    genre = models.CharField(max_length=50, blank=True) # 장르
    nation = models.CharField(max_length=50, blank=True) # 제작국가
    running_time = models.IntegerField(null=True, blank=True) # 상영시간
    release_date = models.DateField(null=True, blank=True) # 개봉일
    ratings = models.CharField(max_length=20, blank=True) # 관람 등급

    synopsis = models.TextField(blank=True) # 줄거리
    keyword = models.CharField(max_length=200, blank=True) # 키워드
    
    status = models.PositiveSmallIntegerField(default=0) # 상영 여부

    avg_grade = models.FloatField(default=0) # 평점
    viewer = models.IntegerField(default=0) # 평점 참여자 수

    cnt_click = models.PositiveBigIntegerField(default=0) # 클릭 수

    def __str__(self) :
        return f'{self.movie_id} - {self.title}'



# 영화 서비스 정보 테이블
class MovieWatch(models.Model) :
    
    movie_id = models.ForeignKey(Movie, related_name='mv_watch', on_delete=models.CASCADE, db_column="movie_id") # 영화 고유 ID
    
    cgv = models.BooleanField(default=0) # CGV 상영 여부
    lotte = models.BooleanField(default=0) # 롯데시네마 상영 여부
    megabox = models.BooleanField(default=0) # 메가박스 상영 여부

    netflix = models.BooleanField(default=0) # 넷플릭스 서비스 여부
    netflix_url = models.CharField(max_length=200) # 넷플릭스 URL

    watcha = models.BooleanField(default=0) # 왓챠 서비스 여부
    watcha_url = models.CharField(max_length=200) # 왓챠 URL

    tving = models.BooleanField(default=0) # 티빙 서비스 여부
    tving_url = models.CharField(max_length=200) # 티빙 URL

    wavve = models.BooleanField(default=0) # 웨이브 서비스 여부
    wavve_url = models.CharField(max_length=200) # 웨이브 URL



# 현재 상영작 테이블
class MovieBoxOffice(models.Model) :

    no = models.PositiveSmallIntegerField(primary_key=True)
    movie_id = models.ForeignKey(Movie, related_name="mv_boxoffice", on_delete=models.CASCADE, db_column="movie_id")

    def __str__(self) :
        return f'{self.pk} -- {self.movie_id}'



# 개봉 예정작 테이블
class MovieUpcoming(models.Model) :

    no = models.PositiveSmallIntegerField(primary_key=True)
    movie_id = models.ForeignKey(Movie, related_name="mv_upcoming", on_delete=models.CASCADE, db_column="movie_id")

    def __str__(self) :
        return f'{self.pk} -- {self.movie_id}'

