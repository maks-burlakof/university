from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users_app.models import User
from users_app.pagination import UsersPageLimitPagination
from users_app.serializers import (
    UserMeOutSerializer,
    UserOutSerializer,
    UserUpdateSerializer,
)


class UserMeView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: UserMeOutSerializer},
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserMeOutSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        request=UserUpdateSerializer,
        responses={
            200: UserMeOutSerializer,
            400: OpenApiResponse(description="Bad Request"),
        },
    )
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_serializer = UserMeOutSerializer(user)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=None,
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserByUsernameView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    lookup_field = "username"

    def get_serializer(self, *args, **kwargs):
        serializer_class = (
            UserMeOutSerializer
            if self.kwargs.get("username") == self.request.user.username
            else UserOutSerializer
        )
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class UserFollowersView(ListAPIView):
    """Get users who follow this user"""

    permission_classes = [AllowAny]
    serializer_class = UserOutSerializer
    pagination_class = UsersPageLimitPagination

    def get_queryset(self):
        if self.kwargs.get("username"):
            user = get_object_or_404(User, username=self.kwargs.get("username"))
        else:
            user = self.request.user
        return user.followers.all()


class UserFollowingView(ListAPIView):
    """Get users that this user is following"""

    permission_classes = [AllowAny]
    serializer_class = UserOutSerializer
    pagination_class = UsersPageLimitPagination

    def get_queryset(self):
        if self.kwargs.get("username"):
            user = get_object_or_404(User, username=self.kwargs.get("username"))
        else:
            user = self.request.user
        return user.following_users.all()


class UserFollowView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={204: None, 400: OpenApiResponse(description="Bad Request")},
    )
    def post(self, request, username, *args, **kwargs):
        if username == request.user.username:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(User, username=username)
        user.followers.add(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        request=None,
        responses={204: None, 400: OpenApiResponse(description="Bad Request")},
    )
    def delete(self, request, username, *args, **kwargs):
        if username == request.user.username:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(User, username=username)
        user.followers.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsersView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserOutSerializer
    pagination_class = UsersPageLimitPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["username", "first_name", "last_name"]
    ordering_fields = ["username", "first_name", "last_name"]


class UsersExploreView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserOutSerializer
    pagination_class = UsersPageLimitPagination

    def get_queryset(self):
        return (
            User.objects.filter(is_allow_recommends=True)
            .exclude(pk__in=self._get_exclude_list(self.request.user))
            .order_by("?")
        )

    @staticmethod
    def _get_exclude_list(user: User) -> list[str]:
        if user.is_authenticated:
            return [user.pk] + list(user.following_users.values_list("pk", flat=True))
        return []
