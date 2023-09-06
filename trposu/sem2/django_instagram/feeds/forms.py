from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import UserProfile, Comment


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Имя',
                                      'class': 'form-control',
                                      'autofocus': ''})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия',
                                      'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя',
                                      'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Email',
                                      'class': 'form-control'})
    )
    password1 = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль',
                                          'class': 'form-control'})
    )
    password2 = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль',
                                          'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя',
                                      'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль',
                                          'class': 'form-control'})
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Имя'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Фамилия'})
    )
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Имя пользователя'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Email'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class UpdateProfileForm(forms.ModelForm):
    # TODO: photo uploading
    description = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Описание профиля'})
    )

    class Meta:
        model = UserProfile
        fields = ['description', 'profile_pic']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Комментарий'})
    )

    class Meta:
        model = Comment
        fields = ['comment']
