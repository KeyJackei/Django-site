from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import CustomUser


class AccountRegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username',  'password1', 'password2')


class AccountLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', )
    password = forms.CharField(label='Пароль', )