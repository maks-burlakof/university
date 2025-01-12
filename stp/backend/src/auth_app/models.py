import uuid

from django.db import models
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import Token
from users_app.models import User


class UserSessions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ipv4 = models.CharField(max_length=128)
    user_agent = models.CharField(max_length=512)

    class Meta:
        unique_together = ("ipv4", "user_agent", "user")
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"

    def __str__(self):
        return self.user.email

    @staticmethod
    def _get_ipv4(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ipv4 = x_forwarded_for.split(",")[-1].strip()
        else:
            ipv4 = request.META.get("REMOTE_ADDR")
        return ipv4

    @staticmethod
    def get_session(request: Request, refresh: str):
        return UserSessions.objects.filter(
            refresh_token=str(refresh).split(".")[-1],
            ipv4=UserSessions._get_ipv4(request),
            user_agent=request.META.get("HTTP_USER_AGENT"),
        ).first()

    @staticmethod
    def update_or_create_session(
        request: Request, user: User, new_refresh: str | Token
    ):
        existing_session = UserSessions.objects.filter(
            user=user,
            ipv4=UserSessions._get_ipv4(request),
            user_agent=request.META.get("HTTP_USER_AGENT"),
        ).first()
        if existing_session:
            existing_session.refresh_token = str(new_refresh).split(".")[-1]
            existing_session.save()
            return existing_session
        else:
            session = UserSessions.objects.create(
                user=user,
                refresh_token=str(new_refresh).split(".")[-1],
                ipv4=UserSessions._get_ipv4(request),
                user_agent=request.META.get("HTTP_USER_AGENT"),
            )
            return session

    @staticmethod
    def delete_session(request: Request, refresh: str | None = None):
        if refresh:
            session = UserSessions.objects.filter(
                refresh_token=str(refresh).split(".")[-1]
            ).first()
            if not session:
                raise UserSessions.DoesNotExist()
            session.delete()
        else:
            session = UserSessions.objects.filter(
                user__id=request.user.id,
                ipv4=UserSessions._get_ipv4(request),
                user_agent=request.META.get("HTTP_USER_AGENT"),
            )
            if not session:
                raise UserSessions.DoesNotExist()
            session.delete()
