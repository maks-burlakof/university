from drf_spectacular.utils import OpenApiResponse, extend_schema
from groups_app.models import Group
from posts_app.models import Comment, Like, Post
from posts_app.models.bookmark import Bookmark
from posts_app.pagination import PostsPageLimitPagination
from posts_app.permission_classes import (
    IsCommentOwner,
    IsPostNotArchivedOrOwner,
    IsPostOwner,
)
from posts_app.serializers import (
    CommentCreateSerializer,
    CommentOutSerializer,
    CommentUpdateSerializer,
    PostCreateSerializer,
    PostOutSelfSerializer,
    PostOutSerializer,
    PostUpdateSerializer,
)
from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.response import Response
from users_app.models import User


class PostCreateView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostCreateSerializer

    @extend_schema(
        request=PostCreateSerializer,
        responses={
            201: PostOutSerializer,
            400: OpenApiResponse(description="Bad Request"),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            user, group = (
                (request.user, None)
                if not serializer.validated_data.get("group")
                else (None, serializer.validated_data.get("group"))
            )
            post = serializer.save(user=user, group=group)
            response_serializer = PostOutSerializer(post)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostView(RetrieveDestroyAPIView):
    queryset = Post.objects.select_related("user", "group").all()
    lookup_url_kwarg = "pk"
    serializer_class = PostOutSerializer

    permission_classes_methods_mapping = {
        "GET": [IsPostNotArchivedOrOwner],
        "PATCH": [IsPostOwner],
        "DELETE": [IsPostOwner],
    }

    def get_permissions(self):
        self.permission_classes = self.permission_classes_methods_mapping.get(
            self.request.method, self.permission_classes
        )
        return super().get_permissions()

    @extend_schema(
        request=PostUpdateSerializer,
        responses={
            200: PostOutSerializer,
            400: OpenApiResponse(description="Bad Request"),
        },
    )
    def patch(self, request, *args, **kwargs):
        serializer = PostUpdateSerializer(
            self.get_object(), data=request.data, partial=True
        )
        if serializer.is_valid():
            post = serializer.save()
            response_serializer = PostOutSerializer(post)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostLikeView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={204: None},
    )
    def post(self, request, pk, *args, **kwargs):
        post: Post = get_object_or_404(Post, pk=pk)
        post.likes.get_or_create(user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        request=None,
        responses={204: None},
    )
    def delete(self, request, pk, *args, **kwargs):
        like = get_object_or_404(Like, user=request.user, post__pk=pk)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostBookmarkView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={204: None},
    )
    def post(self, request, pk, *args, **kwargs):
        post: Post = get_object_or_404(Post, pk=pk)
        post.bookmarks.get_or_create(user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        request=None,
        responses={204: None},
    )
    def delete(self, request, pk, *args, **kwargs):
        bookmark = get_object_or_404(Bookmark, user=request.user, post__pk=pk)
        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostCommentCreateView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=CommentCreateSerializer,
        responses={200: CommentOutSerializer},
    )
    def post(self, request, pk, *args, **kwargs):
        post: Post = get_object_or_404(Post, pk=pk)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(user=request.user, post=post)
            response_serializer = CommentOutSerializer(comment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostCommentView(GenericAPIView):
    queryset = Comment.objects.select_related("user").all()
    lookup_url_kwarg = "comment_pk"

    permission_classes_methods_mapping = {
        "GET": [IsPostNotArchivedOrOwner],
        "PATCH": [IsCommentOwner],
        "DELETE": [IsCommentOwner, IsPostOwner],
    }

    def get_permissions(self) -> list[BasePermission]:
        self.permission_classes = self.permission_classes_methods_mapping.get(
            self.request.method, self.permission_classes
        )
        return super().get_permissions()

    @extend_schema(
        request=None,
        responses={200: CommentOutSerializer},
    )
    def get(self, request, *args, **kwargs):
        serializer = CommentOutSerializer(self.get_object())
        return Response(serializer.data)

    @extend_schema(
        request=CommentUpdateSerializer,
        responses={
            200: CommentOutSerializer,
            400: OpenApiResponse(description="Bad Request"),
        },
    )
    def patch(self, request, *args, **kwargs):
        serializer = CommentUpdateSerializer(
            self.get_object(), data=request.data, partial=True
        )
        if serializer.is_valid():
            comment = serializer.save()
            response_serializer = CommentOutSerializer(comment)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=None,
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostOutSelfSerializer
    pagination_class = PostsPageLimitPagination

    def get_queryset(self):
        username = self.kwargs.get("username")
        groupname = self.kwargs.get("groupname")

        filters = {}
        if username:
            user = get_object_or_404(User, username=username)
            filters["user"] = user
        elif groupname:
            group = get_object_or_404(Group, groupname=groupname)
            filters["group"] = group

        return (
            Post.objects.filter(is_archived=False, **filters)
            .select_related("user")
            .order_by("-created_at")
        )


class PostsExploreView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostOutSerializer
    pagination_class = PostsPageLimitPagination

    def get_queryset(self):
        return (
            Post.objects.filter(is_archived=False)
            .exclude(user__pk__in=self._get_users_exclude_list(self.request.user))
            .select_related("user")
            .order_by("?")
        )

    @staticmethod
    def _get_users_exclude_list(user: User) -> list[str]:
        if user.is_authenticated:
            return [user.pk]
        return []


class PostsFollowingView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostOutSerializer
    pagination_class = PostsPageLimitPagination

    def get_queryset(self):
        return (
            Post.objects.filter(
                user__in=self.request.user.following_users.all(), is_archived=False
            )
            .select_related("user")
            .order_by("-created_at")
        )
