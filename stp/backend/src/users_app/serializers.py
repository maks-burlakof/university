from rest_framework import serializers
from users_app.models import User


class UserBaseOutSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    def get_followers_count(self, obj: User) -> int:
        return obj.followers.count()

    def get_following_count(self, obj: User) -> int:
        return obj.following.count()


class UserMeOutSerializer(UserBaseOutSerializer):
    class Meta:
        model = User
        fields = read_only_fields = [
            "id",
            "email",
            "username",
            "phone_number",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
            "last_login",
            "avatar_color",
            "profile_pic",
            "description",
            "site_url",
            "gender",
            "followers_count",
            "following_count",
            "is_allow_recommends",
        ]


class UserOutSerializer(UserBaseOutSerializer):
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "avatar_color",
            "profile_pic",
            "description",
            "site_url",
            "gender",
            "is_following",
            "followers_count",
            "following_count",
        ]

    def get_is_following(self, obj: User) -> bool:
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.followers.filter(pk=request.user.pk).exists()
        return False


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "phone_number",
            "first_name",
            "last_name",
            "avatar_color",
            "profile_pic",
            "description",
            "site_url",
            "gender",
            "is_allow_recommends",
        ]

    def validate_gender(self, value):
        return value if value else None

    def validate_site_url(self, value):
        return value if value else None

    def validate_profile_pic(self, value):
        if value and value.size > 5 * 1024 * 1024:  # Limit to 5MB
            raise serializers.ValidationError("Image file size must be under 5MB")
        return value
