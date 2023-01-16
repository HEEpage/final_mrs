from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash

from django.views.generic import CreateView, TemplateView, ListView

# from django.contrib.auth.forms import PasswordChangeForm
from .forms import CreateUserForm, ChangeUserForm
from .models import Movie, User, UserMovieLog, UserMovieWish
from .my_page import stats


# 회원가입 view
class UserCreateView(CreateView) :
    form_class = CreateUserForm
    template_name = "users/register.html"
    success_url = reverse_lazy("home")


# 회원 정보 수정 view
def update(request) :

    if request.method == "POST" :
        form = ChangeUserForm(request.POST, instance = request.user)

        if form.is_valid() :
            form.save()
            return redirect('users:user_page')
    else : 
        form = ChangeUserForm(instance = request.user)
        context = {'form' : form}

    return render(request, 'users/update.html', context)


# 비밀번호 수정 view
# def password(request) :

#     if request.method == "POST" :
#         form = PasswordChangeForm(request.POST, instance = request.user)

#         if form.is_valid() :
#             form.save()
#             update_session_auth_hash(request, form.user)

#     else : 
#         form = PasswordChangeForm()
#         context = {'form' : form}

#     return render(request, 'users/update.html', context)


# 마이페이지 view
@method_decorator(login_required, name='dispatch')
class UserPageView(TemplateView) :
    template_name = "users/user_page.html"

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)

        logs = UserMovieLog.objects.filter(user_email__exact = self.request.user.email)
        if logs :
            context['stats'] = stats(logs)

        return context


# 영화 기록 - 확인 view
@login_required(login_url='/accounts/login')
def user_mvlog_view(request) :
    mv_log_list = UserMovieLog.objects.filter(user_email__exact = request.user.email)
    
    return render(request, "users/user_mvlog.html", {'mv_log_list' : mv_log_list})


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

    def get_queryset(self) :
        email =  self.request.user.email

        return UserMovieWish.objects.filter(user_email__exact = email)


# 위시리스트 - 삭제 view
@login_required(login_url='/accounts/login')
def user_wish_delete_view(request, no) :
    wish = UserMovieWish.objects.get(no=no)
    wish.delete()

    return redirect('/accounts/wish/')