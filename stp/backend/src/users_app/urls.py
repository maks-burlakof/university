from django.urls import path
from users_app.views import (
    UserByUsernameView,
    UserFollowersView,
    UserFollowingView,
    UserFollowView,
    UserMeView,
    UsersExploreView,
    UsersView,
)

urlpatterns = [
    path("user/me", UserMeView.as_view(), name="user-me"),
    path("user/<str:username>", UserByUsernameView.as_view(), name="user-by-username"),
    path("user/<str:username>/follow", UserFollowView.as_view(), name="user-follow"),
    path("user/followers/me", UserFollowersView.as_view(), name="user-followers-me"),
    path(
        "user/followers/<str:username>",
        UserFollowersView.as_view(),
        name="user-followers-by-username",
    ),
    path("user/following/me", UserFollowingView.as_view(), name="user-following-me"),
    path(
        "user/following/<str:username>",
        UserFollowingView.as_view(),
        name="user-following-by-username",
    ),
    path("users", UsersView.as_view(), name="users"),
    path("users/explore", UsersExploreView.as_view(), name="users-explore"),
]
