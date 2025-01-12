from core_app.models import BaseModel
from core_app.utils import frontend_url
from django.db.models import CASCADE, CharField, ForeignKey
from posts_app.models.post import Post
from users_app.models import User
from utils.date_utils import get_str_time


class Comment(BaseModel):
    post = ForeignKey(
        to=Post,
        on_delete=CASCADE,
        related_name="comments",
        verbose_name="Publication",
    )
    user = ForeignKey(
        to=User,
        on_delete=CASCADE,
        verbose_name="User",
    )
    comment = CharField(
        max_length=256,
        verbose_name="Comment",
    )

    @property
    def created_ago(self) -> str:
        """Created"""
        return get_str_time(self)

    def get_absolute_url(self) -> str:
        return frontend_url("post", args=[self.post.id])

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
