from auth_app.views import LoginView, LogoutView, RefreshView, SignupView
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/login/refresh", RefreshView.as_view(), name="login-refresh"),
    path("auth/login/verify", TokenVerifyView.as_view(), name="login-verify"),
    path("auth/logout", LogoutView.as_view(), name="logout"),
    path("auth/signup", SignupView.as_view(), name="signup"),
]
