from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .views import views, auth, docs, ajax
from . import forms

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_pk>/', views.post, name='post'),
    path('profile/', views.profile, name='my-profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('explore/', views.explore, name='explore'),
    path('explore/users/', views.explore_users, name='explore-users'),
    path('followers/<str:username>/', views.followers, name='followers'),
    path('following/<str:username>/', views.following, name='following'),
    path('profile/edit/info/', views.profile_settings_info, name='profile-settings'),
    path('profile/edit/security/', auth.ChangePasswordView.as_view(), name='profile-settings-security'),
    path('profile-bookmarks/', views.profile, name='profile-bookmarks'),
    path('post-create/', views.post_picture, name='post-create'),
    path('post/edit/<int:post_pk>/', views.post_edit, name='post-edit'),

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

    # ajax
    path('ajax/validate/username/', ajax.validate_username, name='ajax-validate-username'),
    path('ajax/like/', ajax.like),
    path('ajax/follow/', ajax.follow),
    path('ajax/comment/delete/', ajax.comment_delete),
    path('ajax/bookmark/', ajax.bookmark),
    path('ajax/qr/', ajax.qr_code_generator),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path("__debug__/", include("debug_toolbar.urls")),
