from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from image_uploader_widget.widgets import ImageUploaderWidget

from .models import Profile, Comment, Post
from .scripts import send_email


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Имя',
                                      'class': 'form-control'})
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
                                      'class': 'form-control',
                                      'autofocus': ''})
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


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                       'class': 'form-control'})
    )

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        subject = 'Сброс пароля на Babushka'

        user = context['user']
        del context['user']
        context.update({
            'first_name': user.first_name,
            'username': user.username,
        })

        send_email(
            subject=subject,
            email_template=email_template_name,
            to_email=to_email,
            context=context,
        )


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
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Email'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UpdateProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(
        required=False,
        widget=ImageUploaderWidget(empty_text="Перетащите сюда фото"),
    )
    description = forms.CharField(
        max_length=128,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'style': 'height: 8rem;',
                                     'placeholder': 'О себе'})
    )
    site_url = forms.URLField(
        max_length=128,
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control',
                                     'placeholder': 'Сайт'})
    )
    gender = forms.ChoiceField(
        required=False,
        choices=[('', 'Не указывать'), ('m', 'Мужской'), ('w', 'Женский')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    is_allow_recommends = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Profile
        fields = ['profile_pic', 'description', 'site_url', 'gender', 'is_allow_recommends']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        max_length=256,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'style': 'height: 2rem; font-size: .8rem;',
                                     'placeholder': 'Добавьте комментарий...'})
    )

    class Meta:
        model = Comment
        fields = ['comment']


class PostPictureForm(forms.ModelForm):
    title = forms.CharField(
        max_length=512,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'style': 'height: 10rem;',
                                     'placeholder': 'Добавьте подпись...'})
    )
    image = forms.ImageField(widget=ImageUploaderWidget(
        empty_text="Перетащите сюда фото",
    ))
    is_archived = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    is_allow_comments = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Post
        fields = ['title', 'image', 'is_archived', 'is_allow_comments']


class EditPostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=512,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'style': 'height: 10rem;',
                                     'placeholder': 'Добавьте подпись...'})
    )
    is_archived = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    is_allow_comments = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Post
        fields = ['title', 'is_archived', 'is_allow_comments']
