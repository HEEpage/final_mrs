from django.urls import reverse_lazy

from django.views.generic import CreateView

from .forms import CreateUserForm

# 회원가입 view
class UserCreateView(CreateView) :
    form_class = CreateUserForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("home")


# # 로그인 view
# def signin(request) :
#     if request.method == "POST" :
#         form = LoginUserForm(request.POST)
        
#         email = request.POST["eamil"]
#         password = request.POST["password"]

#         user = authenticate(email = email, password = password)

#         if user is not None :
#             login(request, user)
#             # return redirect("/")
#         else :
#             return HttpResponse("로그인 실패! 다시 시도해 주세요")
    
#     else :
#         form = LoginUserForm()
#         return render(request, "users/signin.html", {"form" : form})


# # 로그아웃 view
# def signout(request) :
#     logout(request)
#     return redirect('/')