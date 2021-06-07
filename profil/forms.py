from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import PasswordInput


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    """Form for login in profile"""
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введіть логін або email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Введіть пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegisterForm(UserCreationForm):
    """Form for registration users"""
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': "Введіть ім'я"}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Введіть прізвище'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Введіть пошту', 'type': 'email'}))

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введіть логін'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Введіть пароль'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Підтвердіть пароль'}))

    field_order = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Емейл вже зараєстрований")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
