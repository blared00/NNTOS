from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Comment, Mark
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50, label='Логин', widget=forms.TextInput(attrs={'class': 'input', 'placeholder': "Введите логин"}))
    password = forms.CharField(max_length=30, min_length=8, label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': "Введите пароль"}))


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].required = False

    class Meta:
        model = Comment
        fields = ['comment', 'student', 'discipline']
        widgets = {
            'comment': forms.Textarea(attrs={"class": "input_sub"}),
            'student': forms.TextInput(attrs={'type': 'text'}),
            'discipline': forms.TextInput(attrs={'type': 'text',}),
        }


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['value', 'discipline', 'student', 'date']


