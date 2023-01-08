from django.contrib import admin
from .models import User, UserMovieLog, UserLogData

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin) :
    list_display = ("email", "username", "birth", "gender", "preference_genre")
    list_filter = ("email",)


admin.site.register(UserMovieLog)
admin.site.register(UserLogData)
