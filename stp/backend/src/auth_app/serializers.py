from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users_app.models import User


class UserSignupSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get("email"),
            username=validated_data.get("username"),
            password=validated_data.get("password"),
            phone_number=validated_data.get("phone_number"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
        )
        return user

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
            "phone_number",
            "first_name",
            "last_name",
        )
        extra_kwargs = {"password": {"write_only": True}}


class UserLoginSerializer(TokenObtainPairSerializer):
    pass


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=False, allow_blank=True)
