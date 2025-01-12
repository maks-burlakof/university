from auth_app.models import UserSessions
from auth_app.serializers import (
    UserLoginSerializer,
    UserLogoutSerializer,
    UserSignupSerializer,
)
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users_app.serializers import UserMeOutSerializer


class SignupView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=UserSignupSerializer,
        responses={
            200: UserMeOutSerializer,
            400: OpenApiResponse(description="Bad Request"),
        },
    )
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        response_serializer = UserMeOutSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        serializer.user.last_login = timezone.now()
        serializer.user.save(update_fields=["last_login"])

        UserSessions.update_or_create_session(
            request, serializer.user, serializer.validated_data.get("refresh")
        )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        serializer = UserLogoutSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            UserSessions.delete_session(
                request, serializer.validated_data.get("refresh")
            )
        except UserSessions.DoesNotExist:
            return Response(
                {"error": "Session not found"}, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(status=status.HTTP_200_OK)


class RefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        session = UserSessions.get_session(request, request.data.get("refresh"))
        if not session:
            return Response(
                {"error": "Session not found"}, status=status.HTTP_401_UNAUTHORIZED
            )

        session.refresh_token = str(response.data["refresh"]).split(".")[-1]
        session.save()
        return response
