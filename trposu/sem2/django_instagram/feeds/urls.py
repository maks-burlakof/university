from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .views import views, auth, docs
from . import forms

urlpatterns = [
    path('', views.index, name='index'),
    path('explore/', views.explore, name='explore'),
    path('profile/', views.my_profile, name='my-profile'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('followers/<str:username>', views.followers, name='followers'),
    path('following/<str:username>', views.following, name='following'),
    path('profile-edit/info/', views.profile_settings_info, name='profile-settings'),
    path('profile-edit/security/', views.profile_settings_security, name='profile-settings-security'),
    path('post-create/', views.post_picture, name='post-create'),

    # auth
    path('login/', auth.CustomLoginView.as_view(
        redirect_authenticated_user=True,
        template_name='auth/login.html',
        authentication_form=forms.LoginForm,
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
    path('registration/', auth.register, name='register'),

    # docs
    path('docs/', docs.index, name='docs-index'),
    path('docs/terms-and-rules/', docs.terms_of_use, name='docs-terms-and-rules'),
    path('docs/dev-tools/', docs.dev_tools, name='docs-dev-tools'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path("__debug__/", include("debug_toolbar.urls")),
