from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash

from django.views.generic import CreateView, TemplateView, ListView, FormView

# from django.contrib.auth.forms import PasswordChangeForm
from users.forms import CreateUserForm, ChangeUserForm
from users.models import User, UserMovieLog, UserMovieWish
from users.my_page import stats
from movies.models import Movie, MovieGenre

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# 회원가입 view
class UserCreateView(FormView) :
    form_class = CreateUserForm
    template_name = "users/register.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['genre_list'] = MovieGenre.objects.all()

        length = len(context['genre_list'])//2 + 1
        context["genre_type1"] = context['genre_list'][:length]
        context["genre_type2"] = context['genre_list'][length:]

        return context

    def post(self, request, *args, **kwargs) :
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, "users/login.html", {'message' : "회원가입 성공 :)"})
        
        else :
            context = {
                'form' : CreateUserForm(),
                'message' : "회원가입 실패! 모두 필수 항목입니다. 올바르게 다시 작성해주세요.",
                'genre_list' : MovieGenre.objects.all(),
            }

            return render(request, "users/register.html", context)
    

# 회원 정보 수정 view
@login_required(login_url='/accounts/login')
def update(request) :

    if request.method == "POST" :
        form = ChangeUserForm(request.POST, instance = request.user)

        if form.is_valid() :
            form.save()

            return render(request, "users/user_page.html")

    else : 
        form = ChangeUserForm(instance = request.user)
        context = {'form' : form}
        context['genre_list'] = MovieGenre.objects.all()

        genre_list = MovieGenre.objects.all()
        length = len(genre_list)//2 + 1

        context["genre_type1"] = genre_list[:length]
        context["genre_type2"] = genre_list[length:]

        return render(request, "users/update.html", context)


# 마이페이지 view
@method_decorator(login_required, name='dispatch')
class UserPageView(TemplateView) :
    template_name = "users/user_page.html"

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['username'] = User.objects.get(email = self.request.user.email).username

        logs = UserMovieLog.objects.filter(user_email__exact = self.request.user.email)
        if logs :
            context['stats'] = stats(logs)
        
        genre_list = MovieGenre.objects.all()
        length = len(genre_list)//2 + 1

        context["genre_type1"] = genre_list[:length]
        context["genre_type2"] = genre_list[length:]

        return context


# 영화 기록 - 확인 view
@login_required(login_url='/accounts/login')
def user_mvlog_view(request) :
    mv_log_list = UserMovieLog.objects.filter(user_email__exact = request.user.email)

    context = {
        'mv_log_list' : mv_log_list
    }

    genre_list = MovieGenre.objects.all()
    length = len(genre_list)//2 + 1

    context["genre_type1"] = genre_list[:length]
    context["genre_type2"] = genre_list[length:]

    return render(request, "users/user_mvlog.html", context)


# 영화 기록 - 조회 view
@login_required(login_url='/accounts/login')
def user_mvlog_search_view(request) :

    if request.POST :
        keyword = request.POST['keyword']
        movie_list = Movie.objects.filter(title__icontains = keyword)

        return render(request, "users/user_mvlog_add.html", {'movie_list':movie_list} )


# 영화 기록 - 등록 view
@login_required(login_url='/accounts/login')
def user_mvlog_add_view(request) :

    if request.POST :
        id = request.POST['id']
        movie = Movie.objects.get(id = id)

        return render(request, "users/user_mvlog_add.html", {'movie':movie})
    
    else :

        return render(request, "users/user_mvlog_add.html")


# 영화 기록 - 작성 view
@login_required(login_url='/accounts/login')
def user_mvlog_write_view(request) :
    
    if request.POST :

        log = {
            "user_email" : User.objects.get(email = request.user.email),
            "movie_id" : Movie.objects.get(id = request.POST['id']),
            "grade" : request.POST['grade'],
            "review" : request.POST['review']
        }
        UserMovieLog(**log).save()

        return redirect('/accounts/mv-log/')


# 영화 기록 - 삭제 view
@login_required(login_url='/accounts/login')
def user_mvlog_delete_view(request, no) :
    log = UserMovieLog.objects.get(no=no)
    log.delete()

    return redirect('/accounts/mv-log/')


# 위시리스트 view
@method_decorator(login_required, name='dispatch')
class UserWishView(ListView) :
    model = UserMovieWish
    template_name = "users/user_wish.html"

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)

        genre_list = MovieGenre.objects.all()
        length = len(genre_list)//2 + 1

        context["genre_type1"] = genre_list[:length]
        context["genre_type2"] = genre_list[length:]

        return context


    def get_queryset(self) :
        email =  self.request.user.email

        return UserMovieWish.objects.filter(user_email__exact = email)


# 위시리스트 - 삭제 view
@login_required(login_url='/accounts/login')
def user_wish_delete_view(request, no) :
    wish = UserMovieWish.objects.get(no=no)
    wish.delete()

    return redirect('/accounts/wish/')


# email 중복 체크
@csrf_exempt
def checked_email(request) :
    email = request.POST.get('email', '')

    try :
        user = User.objects.get(email = email)
    except Exception as e :
        user = None

    return JsonResponse({
        'result' : 'not exist' if user is None else 'exist',
    })


# username 중복 체크
@csrf_exempt
def checked_username(request) :
    name = request.POST.get('username', '')

    try :
        user = User.objects.get(username = name)
    except Exception as e :
        user = None

    return JsonResponse({
        'result' : 'not exist' if user is None else 'exist',
    })
