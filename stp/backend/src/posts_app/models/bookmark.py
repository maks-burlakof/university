from uuid import uuid4

from django.db.models import CASCADE, DateTimeField, ForeignKey, Model, UUIDField
from django.utils import timezone
from posts_app.models.post import Post
from users_app.models import User


class Bookmark(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    post = ForeignKey(
        to=Post,
        on_delete=CASCADE,
        related_name="bookmarks",
    )
    user = ForeignKey(
        to=User,
        on_delete=CASCADE,
    )
    created_at = DateTimeField(db_index=True, default=timezone.now)

    class Meta:
        unique_together = ("post", "user")
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"
