from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.views.generic import TemplateView
from django.contrib.auth import authenticate

from .forms import *


class LoginUserView(LoginView):
    form_class = AccountLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_user_context(self, **kwargs):
        context = kwargs

        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")

        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse('main')



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


def register(request):
    if request.method == 'POST':
        form = AccountRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = AccountRegisterForm()
    return render(request, 'users/register.html', {'form': form})