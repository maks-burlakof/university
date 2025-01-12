from uuid import uuid4

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import (
    DO_NOTHING,
    CharField,
    ImageField,
    ManyToManyField,
    Model,
    OneToOneField,
    URLField,
    UUIDField,
)
from users_app.models import User


class Group(Model):
    is_update_image = False

    def img_path(self, filename) -> str:
        return "%s/%s" % (self.groupname, filename)

    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    groupname = CharField(
        max_length=20,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": "This group already exists.",
        },
        verbose_name="Groupname",
    )
    title = CharField(
        max_length=64,
        verbose_name="Title",
    )
    owner = OneToOneField(
        to=User,
        on_delete=DO_NOTHING,
        related_name="owned_group",
        verbose_name="Owner user",
    )
    followers = ManyToManyField(
        to=User,
        blank=True,
        related_name="followed_groups",
        verbose_name="Followers",
    )
    profile_pic = ImageField(
        upload_to=img_path,
        null=True,
        blank=True,
        verbose_name="Profile picture",
    )
    description = CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name="Description",
    )
    site_url = URLField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name="Website url",
    )

    def save(self, *args, **kwargs):
        super(Group, self).save(*args, **kwargs)
        if self.is_update_image:
            # image_compressor.compress_image(self.image.path)
            self.is_update_image = False

    # def get_absolute_url(self):
    #     return reverse("group", args=[self.groupname])

    # def get_edit_absolute_url(self):
    #     return reverse("group-settings", args=[self.groupname])

    def __str__(self):
        return self.groupname

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
