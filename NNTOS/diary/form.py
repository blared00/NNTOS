from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50, label='Логин', widget=forms.TextInput(attrs={'class': 'input', 'placeholder': "Введите логин"}))
    password = forms.CharField(max_length=30, min_length=8, label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': "Введите пароль"}))


class CommentForm(forms.Form):
    text = forms.CharField(max_length=50)
