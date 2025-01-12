from posts_app.models import Comment, Post
from rest_framework.permissions import IsAuthenticated


class IsPostOwner(IsAuthenticated):
    """
    Allows access only to a post owner user.
    """

    def has_object_permission(self, request, view, obj: Post | Comment):
        obj_class_post_mapping = {
            Post: lambda: obj,
            Comment: lambda: obj.post,
        }

        post: Post = obj_class_post_mapping.get(type(obj))()
        if not post:
            raise ValueError(
                f"IsPostOwner permission class can be used only with "
                f"{obj_class_post_mapping.keys()} objects"
            )

        if post.user:
            owner = post.user
        elif post.group:
            owner = post.group.owner
        else:
            return False
        return owner == request.user


class IsPostNotArchivedOrOwner(IsAuthenticated):
    """
    Allows access only to a post owner user or a user that is not archived.
    """

    def has_object_permission(self, request, view, obj: Post | Comment):
        obj_class_post_mapping = {
            Post: lambda: obj,
            Comment: lambda: obj.post,
        }

        post: Post = obj_class_post_mapping.get(type(obj))()
        if not post:
            raise ValueError(
                f"IsPostNotArchivedOrOwner permission class can be used only with "
                f"{obj_class_post_mapping.keys()} objects"
            )

        if not post.is_archived:
            return True
        else:
            return IsPostOwner().has_object_permission(request, view, obj)


class IsCommentOwner(IsAuthenticated):
    """
    Allows access only to a comment owner user.
    """

    def has_object_permission(self, request, view, obj: Comment):
        if not isinstance(obj, Comment):
            raise ValueError(
                "IsCommentOwner permission class can be used only with Comment objects"
            )

        return obj.user == request.user
