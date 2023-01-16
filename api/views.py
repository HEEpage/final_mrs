from django.shortcuts import render

from movies.models import Movie, MovieGenre, MovieReviewDummy
from users.models import UserMovieLog, UserMovieWish
from api.serializers import MovieSerializers, MovieReviewSerializers, UserMoiveLogSerializers, ReviewCreateSerializer

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.generics import CreateAPIView

from rest_framework import status, viewsets


class MovieListAPI(APIView):

    def get(self, request):
        paramGenre = self.request.GET.get('genre')
        paramSort = self.request.GET.get('sort')

        if paramGenre:
            genre = MovieGenre.objects.get(no=paramGenre).type
            queryset = Movie.objects.filter(genre__contains=genre)

            if paramSort == "1":
                queryset = Movie.objects.filter(genre__contains=genre).order_by('-cnt_click')
            
            elif paramSort == "2":
                queryset = Movie.objects.filter(genre__contains=genre).order_by('-release_date')
       
        else:
            queryset = Movie.objects.all()

        serializer = MovieSerializers(queryset, many=True)
        
        return Response(serializer.data)


class MovieDetailAPI(APIView):

    def get(self, request):
        paramId = self.request.GET.get('code')
        print(paramId)

        queryset = Movie.objects.get(id=paramId)

        serializer = MovieSerializers(queryset, many=False)

        return Response(serializer.data)


# 영화 리뷰 더미데이터 목록
class ReviewDummyListAPI(APIView):
    
    def get(self, request):
        paramId = self.request.GET.get('code')
        print(paramId)

        queryset = MovieReviewDummy.objects.get(movie_id=paramId)

        serializer = MovieReviewSerializers(queryset, many=False)

        return Response(serializer.data)



# 유저 영화 기록 목록 및 생성
class UserMovieLogAPI(APIView):
    
    def get(self, request):
        reviews = UserMovieLog.objects.all()

        serializer = UserMoiveLogSerializers(reviews, many=True)

        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserMoiveLogSerializers(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

