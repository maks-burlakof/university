from django.urls import path
from django.contrib.auth import views as auth_views

from .views import views, auth
from . import forms

urlpatterns = [
    path('', views.index, name='index'),
    path('explore/', views.explore, name='explore'),
    path('profile/', views.my_profile, name='my-profile'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('followers/<str:username>', views.followers, name='followers'),
    path('following/<str:username>', views.following, name='following'),
    path('profile-edit/', views.profile_settings, name='profile-settings'),

    # auth
    path('login/', auth.CustomLoginView.as_view(
        redirect_authenticated_user=True,
        template_name='auth/login.html',
        authentication_form=forms.LoginForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
    path('registration/', auth.register, name='register'),
]
