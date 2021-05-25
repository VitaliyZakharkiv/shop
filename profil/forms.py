from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    """Form for login in profile"""
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введіть логін'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Введіть пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegisterForm(UserCreationForm):
    """Form for registration users"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введіть логін'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Введіть ім'я"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введіть прізвище'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введіть пошту', 'type': 'email'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Введіть пароль'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Підтвердіть пароль'}))

    field_order = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
