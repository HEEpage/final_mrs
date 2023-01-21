from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.http import Http404

from api.serializers import MovieSerializers, MovieReviewSerializers, UserMoiveLogSerializers, UserMovieWishSerializers
from api.permission import IsOwnerOrReadOnly
from movies.models import Movie, MovieGenre, MovieReviewDummy
from users.models import UserMovieLog, UserMovieWish


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


# 사용자 영화 기록 목록 및 생성 - 영화 디테일 페이지
class UserMovieLogAPI(APIView):
    
    # 영화 리뷰 데이터 목록
    def get(self, request):
        paramMV = self.request.GET.get('code')
        reviews = UserMovieLog.objects.filter(movie_id__exact = paramMV)

        serializer = UserMoiveLogSerializers(reviews, many=True)

        return Response(serializer.data)

    # 영화 디테일 페이지 내 사용자 평점 및 리뷰 기록 작성
    def post(self, request):
        serializer = UserMoiveLogSerializers(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 사용자 영화 기록 목록 및 생성 - 마이페이지
class UserLogAPI(APIView):
    
    # # authentication
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    # # permission
    # permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # 사용자의 영화 기록 조회
    def get(self, request):
        email = request.user.email
        reviews = UserMovieLog.objects.filter(user_email__exact = email)

        serializer = UserMoiveLogSerializers(reviews, many=True)

        return Response(serializer.data)
    
    # 영화 기록 작성
    def post(self, request):
        serializer = UserMoiveLogSerializers(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 사용자 영화 특정 기록 조회, 수정, 삭제 - 마이페이지
class UserLogDetailAPI(APIView):

    # # authentication
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    # # permission
    # permission_classes = [IsAuthenticatedOrReadOnly]
    
    # 기록 객체 가져오기
    def get_object(self, no):
        try: return UserMovieLog.objects.get(no = no)
        except UserMovieLog.DoesNotExist: raise Http404
    
    # 특정 기록 조회
    def get(self, request, no, format = None) :
        review = self.get_object(no)
        serialiszer = UserMoiveLogSerializers(review, many=False)

        return Response(serialiszer.data)

    # 특정 기록 수정
    def put(self, request, no, format = None) :
        review = self.get_object(no)
        serializer = UserMoiveLogSerializers(review, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 특정 기록 삭제
    def delete(self, request, no, format = None) :
        review = self.get_object(no)
        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


# 사용자 영화 위시리스트 조회
class UserWishAPI(APIView):

    # 위시리스트 조회
    def get(self, request):
        email = request.user.email
        wish = UserMovieWish.objects.filter(user_email__exact = email)

        serializer = UserMovieWishSerializers(wish, many=True)

        return Response(serializer.data)
    
    # 위시리스트에 영화 등록
    def post(self, request):
        serializer = UserMovieWishSerializers(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 사용자 영화 위시리스트 특정 기록 조회, 수정, 삭제 - 마이페이지
class UserWishDetailAPI(APIView) :

    # 위시리스트 객체 가져오기
    def get_object(self, no):
        try: return UserMovieWish.objects.get(no = no)
        except UserMovieWish.DoesNotExist: raise Http404
    
    # 특정 위시리스트 조회
    def get(self, request, no, format = None) :
        wish = self.get_object(no)
        serialiszer = UserMovieWishSerializers(wish, many=False)

        return Response(serialiszer.data)

    # 위시리스트의 특정 영화 삭제
    def delete(self, request, no, format = None) :
        wish = self.get_object(no)
        wish.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

