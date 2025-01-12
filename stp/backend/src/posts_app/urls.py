from django.urls import path
from posts_app.views import (
    PostBookmarkView,
    PostCommentCreateView,
    PostCommentView,
    PostCreateView,
    PostLikeView,
    PostsExploreView,
    PostsFollowingView,
    PostsView,
    PostView,
)

urlpatterns = [
    path("post", PostCreateView.as_view(), name="post-create"),
    path("post/<uuid:pk>", PostView.as_view(), name="post-by-id"),
    path("post/<uuid:pk>/like", PostLikeView.as_view(), name="post-like"),
    path("post/<uuid:pk>/bookmark", PostBookmarkView.as_view(), name="post-bookmark"),
    path(
        "post/<uuid:pk>/comment",
        PostCommentCreateView.as_view(),
        name="post-comment-create",
    ),
    path(
        "post/<uuid:post_pk>/comment/<uuid:comment_pk>",
        PostCommentView.as_view(),
        name="post-comment-by-id",
    ),
    path("posts/explore", PostsExploreView.as_view(), name="posts-explore"),
    path("posts/following", PostsFollowingView.as_view(), name="posts-following"),
    path("posts/user/<str:username>", PostsView.as_view(), name="posts-user"),
    path("posts/group/<str:groupname>", PostsView.as_view(), name="posts-group"),
]
