from core_app.models import BaseModel
from core_app.utils import frontend_url
from django.db.models import CASCADE, BooleanField, CharField, ForeignKey, ImageField
from groups_app.models import Group
from users_app.models import User
from utils.date_utils import get_str_time


class Post(BaseModel):
    def img_path(self, filename) -> str:
        if self.user:
            return f"posts/users/{self.user.username}/{filename}"
        elif self.group:
            return f"posts/groups/{self.group.groupname}/{filename}"
        else:
            return f"posts/unlinked/{filename}"

    user = ForeignKey(
        to=User,
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name="User",
    )
    group = ForeignKey(
        to=Group,
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name="Group",
    )
    title = CharField(
        max_length=512,
        blank=True,
        null=True,
        verbose_name="Description",
    )
    image = ImageField(
        upload_to=img_path,
        verbose_name="Picture",
    )
    is_archived = BooleanField(
        default=False,
        verbose_name="Archived",
    )
    is_allow_comments = BooleanField(
        default=True,
        verbose_name="Allow comments",
    )

    def save(self, *args, **kwargs) -> None:
        if self.user and self.group:
            raise ValueError(
                "Post object cannot have a linked Profile and a Group at the same time"
            )
        if not self.user and not self.group:
            raise ValueError("Post object must have a linked Profile or a Group")
        else:
            super(Post, self).save(*args, **kwargs)

    @property
    def created_ago(self) -> str:
        """Created"""
        return get_str_time(self)

    @property
    def likes_num(self) -> int:
        """Liked"""
        return self.likes.count()

    @property
    def comments_num(self) -> int | None:
        """Comments"""
        if self.is_allow_comments:
            return self.comments.count()
        else:
            return None

    @property
    def bookmarks_num(self) -> int:
        """In bookmarks"""
        return self.bookmarks.count()

    def is_user_liked(self, user: User) -> bool:
        return self.likes.filter(user=user).exists()

    def is_user_bookmarked(self, user: User) -> bool:
        return self.bookmarks.filter(user=user).exists()

    def get_absolute_url(self) -> str:
        return frontend_url("post", args=[self.id])

    def __str__(self):
        return f"{self.user}, {self.title}"

    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
