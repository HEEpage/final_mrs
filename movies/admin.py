from django.contrib import admin
from .models import Movie, MovieWatch, MovieBoxOffice, MovieUpcoming, MovieReviewDummy

# Register your models here.
admin.site.register(Movie)
admin.site.register(MovieWatch)
admin.site.register(MovieBoxOffice)
admin.site.register(MovieUpcoming)
admin.site.register(MovieReviewDummy)
