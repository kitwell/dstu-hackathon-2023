from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import *

def login_user(request):
    context = {'login_form': LoginForm()}
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')

            else:
                context ={'login_form': login_form, 'attention': f'Пользователь с именем {username} не был найден'}

    return render(request, 'users/login.html', context)


class Register(TemplateView):
    template_name = 'users/register.html'

    def get(self, request):
        user_add = RegisterForm()
        context = {'user_add': user_add}
        return render(request, 'users/register.html', context)

    def post(self, request):
        user_add = RegisterForm(request.POST)
        if user_add.is_valid():
            user = user_add.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('index')

        context = {'user_add': user_add}
        return render(request, 'users/register.html', context)
