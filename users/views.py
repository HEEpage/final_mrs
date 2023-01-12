from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import CreateView

from .forms import CreateUserForm

# 회원가입 view
class UserCreateView(CreateView) :
    form_class = CreateUserForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('home')