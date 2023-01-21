from rest_framework import serializers
from movies.models import Movie, MovieUpcoming, MovieBoxOffice, MovieReviewDummy, MovieWatch
from users.models import UserMovieLog, UserMovieWish


class BoxOfficeSerializers(serializers.ModelSerializer) :
    class Meta :
        model = MovieBoxOffice
        fields = ('__all__')

    def to_representation(self, instance):
        self.fields['movie_id'] = MovieSerializers(read_only=True)
        return super(BoxOfficeSerializers, self).to_representation(instance)


class UpcomingSerializers(serializers.ModelSerializer) :
    class Meta :
        model = MovieUpcoming
        fields = ('__all__')
    
    def to_representation(self, instance):
        self.fields['movie_id'] = MovieSerializers(read_only=True)
        return super(UpcomingSerializers, self).to_representation(instance)


class MovieSerializers(serializers.ModelSerializer) :
    class Meta :
        model = Movie
        fields = ('__all__')


class MovieReviewSerializers(serializers.ModelSerializer) :
    class Meta :
        model = MovieReviewDummy
        fields = ('__all__')


class UserMoiveLogSerializers(serializers.ModelSerializer):
    class Meta:
        model= UserMovieLog
        fields = ('__all__')


class UserMovieWishSerializers(serializers.ModelSerializer) :
    class Meta :
        model = UserMovieWish
        fields = ('__all__')