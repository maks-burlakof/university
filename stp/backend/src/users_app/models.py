import random
from uuid import uuid4

from core_app.utils import frontend_url
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import QuerySet, UUIDField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    is_update_image = False

    def img_path(self, filename) -> str:
        return f"users/{self.username}/{filename}"

    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=64,
        unique=True,
        validators=[UnicodeUsernameValidator()],
    )
    phone_number = models.CharField(max_length=16)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    avatar_color = models.CharField(max_length=7)
    followers = models.ManyToManyField(
        to="User",
        null=True,
        blank=True,
        verbose_name="Followers",
    )
    profile_pic = models.ImageField(
        upload_to=img_path,
        null=True,
        blank=True,
        verbose_name="Profile picture",
    )
    description = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name="About",
    )
    site_url = models.URLField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name="Website",
    )
    gender = models.CharField(
        max_length=1,
        choices=[("m", "Male"), ("w", "Female")],
        null=True,
        blank=True,
        verbose_name="Gender",
    )
    is_allow_recommends = models.BooleanField(
        default=True,
        verbose_name="Allow to recommend profile",
    )
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        null=True,
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",
        null=True,
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "password",
    ]

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs) -> None:
        if not self.avatar_color:
            self.avatar_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        # Delete image from S3 storage if it was changed or deleted
        if self.pk:
            try:
                old_image = User.objects.get(pk=self.pk).profile_pic
                if old_image and self.profile_pic != old_image:
                    old_image.delete(save=False)
            except User.DoesNotExist:
                pass

        if self.is_update_image:
            # image_compressor.compress_image(self.image.path)
            self.is_update_image = False

        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return frontend_url("user", args=[self.username])

    @property
    def following_users(self) -> QuerySet:
        """
        Get users that this user is following
        """
        return User.objects.filter(followers=self)

    @property
    def following_groups(self) -> QuerySet:
        """
        Get groups that this user is following
        """
        return Group.objects.filter(followers=self).select_related("owner")

    @property
    def following(self) -> QuerySet:
        """
        Get users and groups that this user is following
        """
        return User.objects.filter(followers=self)  # TODO: Add groups

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
