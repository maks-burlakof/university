from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage


class Profile(models.Model):
    is_update_image = False

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
        max_length=128,
        null=True,
        blank=True,
        verbose_name='О себе',
    )
    site_url = models.URLField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='Сайт',
    )
    gender = models.CharField(
        max_length=1,
        choices=[('m', 'Мужской'), ('w', 'Женский')],
        null=True,
        blank=True,
        verbose_name='Пол',
    )

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        if self.is_update_image:
            # image_compressor.compress_image(self.image.path)
            self.is_update_image = False

    def get_profile_pic(self):
        if self.profile_pic:
            return self.profile_pic.url
        return staticfiles_storage.url('img/profile_default.jpg')

    def get_number_of_followers(self):
        return self.followers.count()

    def get_number_of_following(self):
        return self.following.count()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Post(models.Model):
    def img_path(self, filename):
        return '%s/%s' % (self.user_profile.user.username, filename)

    user_profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    title = models.CharField(
        max_length=256,
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
        default=False,
        verbose_name='В архиве',
    )
    is_allow_comments = models.BooleanField(
        default=True,
        verbose_name='Разрешить комментарии',
    )

    def get_str_time(self):
        days = (datetime.now().astimezone() - self.created).days
        if days == 0:
            return 'Сегодня'
        elif days == 1:
            return 'Вчера'
        elif days == 2:
            return 'Позавчера'
        else:
            return f'{days} дн.'

    def get_num_of_likes(self):
        return self.like_set.count()

    def get_num_of_comments(self):
        return self.comment_set.count()

    def __str__(self):
        return f'{self.user_profile}, {self.created}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


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

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Like(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return 'Лайк: ' + self.user.username + ' ' + self.post.title

    class Meta:
        unique_together = ("post", "user")
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
