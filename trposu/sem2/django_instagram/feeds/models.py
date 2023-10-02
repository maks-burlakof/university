from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


def get_user_absolute_url(self):
    return reverse('profile', args=[self.username])


def get_user_str(self):
    return self.username


User.add_to_class("__str__", get_user_str)
User.add_to_class("get_absolute_url", get_user_absolute_url)


def get_str_time(self):
    days = (datetime.now().astimezone() - self.created).days
    if days == 0:
        seconds = (datetime.now().astimezone() - self.created).seconds
        if 0 <= seconds < 5:
            return 'только что'
        if seconds < 60:
            return f'{seconds} сек.'
        elif 0 < seconds // 60 < 60:
            return f'{seconds // 60} мин.'
        else:
            return f'{seconds // 60 // 60} ч.'
    elif days == 1:
        return 'Вчера'
    elif days == 2:
        return 'Позавчера'
    else:
        return f'{days} дн.'


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
    bookmarks = models.ManyToManyField(
        to='Post',
        related_name="bookmarks_profile",
        blank=True,
        verbose_name='Сохраненное',
    )
    profile_pic = models.ImageField(
        upload_to=img_path,
        null=True,
        blank=True,
        verbose_name='Фото профиля',
    )
    description = models.CharField(
        max_length=256,
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
    is_allow_recommends = models.BooleanField(
        default=True,
        verbose_name='Рекомендовать профиль',
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

    def get_following_users_groups(self):
        following_users = User.objects.filter(profile__followers=self).select_related('profile')
        following_groups = Group.objects.filter(followers=self).select_related('owner')
        return following_users, following_groups

    def get_followers(self):
        return self.followers.all()

    def get_absolute_url(self):
        return reverse('profile', args=[self.user.username])

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Group(models.Model):
    is_update_image = False

    def img_path(self, filename):
        return '%s/%s' % (self.groupname, filename)

    groupname = models.CharField(
        max_length=20,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": "Такое сообщество уже существует.",
        },
        verbose_name='Никнейм',
    )
    title = models.CharField(
        max_length=64,
        verbose_name='Название',
    )
    owner = models.OneToOneField(
        to=User,
        on_delete=models.DO_NOTHING,
        verbose_name='Владелец',
    )
    followers = models.ManyToManyField(
        to='Profile',
        blank=True,
        verbose_name='Подписчики',
    )
    profile_pic = models.ImageField(
        upload_to=img_path,
        null=True,
        blank=True,
        verbose_name='Фото сообщества',
    )
    description = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='О сообществе',
    )
    site_url = models.URLField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='Сайт',
    )

    def save(self, *args, **kwargs):
        super(Group, self).save(*args, **kwargs)
        if self.is_update_image:
            # image_compressor.compress_image(self.image.path)
            self.is_update_image = False

    def get_profile_pic(self):
        if self.profile_pic:
            return self.profile_pic.url
        return staticfiles_storage.url('img/group_default.png')

    def get_absolute_url(self):
        return reverse('group', args=[self.groupname])

    def get_edit_absolute_url(self):
        return reverse('group-settings', args=[self.groupname])

    def __str__(self):
        return self.groupname

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'


class Post(models.Model):
    def img_path(self, filename):
        if self.user_profile:
            return '%s/%s' % (self.user_profile.user.username, filename)
        elif self.group:
            return '%s/%s' % (self.group.groupname, filename)
        else:
            return '/'

    user_profile = models.ForeignKey(
        to=Profile,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    group = models.ForeignKey(
        to=Group,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Сообщество',
    )
    title = models.CharField(
        max_length=512,
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

    def save(self, *args, **kwargs):
        if self.user_profile and self.group:
            raise ValueError("Post object cannot have a linked Profile and a Group at the same time")
        else:
            super(Post, self).save(*args, **kwargs)

    def get_str_time(self):
        return get_str_time(self)

    def get_num_of_likes(self):
        return self.likes.count()

    def get_num_of_comments(self):
        return self.comments.count()

    def get_num_of_bookmarks(self):
        return self.bookmarks_profile.count()

    get_str_time.short_description = 'Создан'
    get_num_of_likes.short_description = 'Лайков'
    get_num_of_comments.short_description = 'Комментариев'
    get_num_of_bookmarks.short_description = 'В закладках'

    def is_user_liked(self, user):
        # return self.likes.filter(user=user).exists()
        return self.likes.filter(user=user).exists()

    def is_user_bookmarks(self, user):
        return self.bookmarks_profile.filter(user=user).exists()

    def get_absolute_url(self):
        return reverse('post', args=[self.pk])

    def get_edit_absolute_url(self):
        return reverse('post-edit', args=[self.pk])

    def __str__(self):
        return f'{self.user_profile}, {self.created}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация',
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    comment = models.CharField(
        max_length=256,
        verbose_name='Комментарий',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        verbose_name='Дата создания',
    )

    def get_str_time(self):
        return get_str_time(self)

    get_str_time.short_description = 'Время'

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Like(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Лайк {self.user.username} на пост {self.post.user_profile} #{self.post.pk}'

    class Meta:
        unique_together = ("post", "user")
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
