from uuid import uuid4

from django.db.models import CASCADE, DateTimeField, ForeignKey, Model, UUIDField
from django.utils import timezone
from posts_app.models.post import Post
from users_app.models import User


class Like(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    post = ForeignKey(
        to=Post,
        on_delete=CASCADE,
        related_name="likes",
    )
    user = ForeignKey(
        to=User,
        on_delete=CASCADE,
    )
    created_at = DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("post", "user")
        verbose_name = "Like"
        verbose_name_plural = "Likes"
