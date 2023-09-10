from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    def img_path(self, filename):
        return '%s/%s' % (self.user.username, filename)

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
    )
    followers = models.ManyToManyField(
        to='Profile',
        related_name="followers_profile",
        blank=True,
        verbose_name='Подписчики',
    )
    following = models.ManyToManyField(
        to='Profile',
        related_name="following_profile",
        blank=True,
        verbose_name='Подписки',
    )
    profile_pic = models.ImageField(
        upload_to=img_path,
        verbose_name='Фото профиля',
    )
    description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    def get_number_of_followers(self):
        return self.followers.count()

    def get_number_of_following(self):
        return self.following.count()

    def __str__(self):
        return self.user.username


class Post(models.Model):
    def img_path(self, filename):
        return '%s/%s' % (self.user_profile.user.username, filename)

    user_profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Описание',
    )
    image = models.ImageField(
        upload_to=img_path,
        verbose_name='Фотография',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        verbose_name='Дата создания',
    )
    is_archived = models.BooleanField(
        default=True,
        verbose_name='В архиве',
    )

    def get_number_of_likes(self):
        return self.like_set.count()

    def get_number_of_comments(self):
        return self.comment_set.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    comment = models.CharField(
        max_length=100,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        verbose_name='Дата создания',
    )

    def __str__(self):
        return self.comment


class Like(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return 'Лайк: ' + self.user.username + ' ' + self.post.title
