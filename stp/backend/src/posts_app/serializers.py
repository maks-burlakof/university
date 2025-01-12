from groups_app.serializers import GroupOutSerializer
from posts_app.models import Comment, Post
from rest_framework import serializers
from users_app.serializers import UserOutSerializer


class PostBaseOutSerializer(serializers.ModelSerializer):
    is_user_liked = serializers.SerializerMethodField()
    is_user_bookmarked = serializers.SerializerMethodField()

    def get_is_user_liked(self, obj: Post) -> bool:
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.is_user_liked(request.user)
        return False

    def get_is_user_bookmarked(self, obj: Post) -> bool:
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.is_user_bookmarked(request.user)
        return False


class PostOutSerializer(PostBaseOutSerializer):
    user = UserOutSerializer()
    group = GroupOutSerializer()

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "group",
            "title",
            "image",
            "created_at",
            "likes_num",
            "is_user_liked",
            "bookmarks_num",
            "is_user_bookmarked",
            "is_allow_comments",
            "comments_num",
        ]


class PostOutSelfSerializer(PostBaseOutSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "image",
            "created_at",
            "is_allow_comments",
            "likes_num",
            "is_user_liked",
            "bookmarks_num",
            "is_user_bookmarked",
            "is_allow_comments",
            "comments_num",
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "group",
            "title",
            "image",
            "is_allow_comments",
        ]

        def validate_image(self, value):
            if value.size > 10 * 1024 * 1024:  # Limit to 5MB
                raise serializers.ValidationError("Image file size must be under 10MB")
            return value


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "is_allow_comments",
        ]


class CommentOutSerializer(serializers.ModelSerializer):
    user = UserOutSerializer()

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "comment",
            "created_at",
        ]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "comment",
        ]


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "comment",
        ]
