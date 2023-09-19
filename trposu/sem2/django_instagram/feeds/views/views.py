from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from feeds.models import Profile, Post, Like, Comment
from feeds.forms import UpdateProfileForm, UpdateUserForm, PostPictureForm, CommentForm, EditPostForm

POSTS_ON_PAGE = 30


def add_posts_likes(user: User, posts):
    if user.is_authenticated:
        if type(posts) == Post:
            posts.is_liked = posts.is_user_liked(user)
            posts.is_bookmark = posts.is_user_bookmarks(user)
        else:
            for post in posts:
                post.is_liked = post.is_user_liked(user)
                post.is_bookmark = post.is_user_bookmarks(user)


def get_recommended_users(request, user_exclude=None):
    id_list = []
    if request.user.is_authenticated:
        id_list = [request.user.pk]
        if user_exclude:
            id_list.append(user_exclude)

    return User.objects.filter(profile__is_allow_recommends=True).exclude(pk__in=id_list).select_related('profile').order_by('?')


def index(request):
    if request.user.is_authenticated:
        user = request.user
        users_followed = request.user.profile.following.all()
        posts = Post.objects.filter(
            Q(user_profile__in=users_followed) |
            Q(user_profile=user.profile),
            is_archived=False,
        ).select_related('user_profile', 'user_profile__user').prefetch_related('like_set').order_by('-created')[:POSTS_ON_PAGE]
        add_posts_likes(user, posts)
    else:
        posts = Post.objects.filter(is_archived=False).select_related('user_profile', 'user_profile__user').order_by('?')[:POSTS_ON_PAGE]

    recommended_users = get_recommended_users(request)[:5]

    context = {
        'posts': posts,
        'recommended_users': recommended_users,
    }

    return render(request, 'index.html', context)


def explore(request):
    random_posts = Post.objects.filter(is_archived=False).order_by('?')[:40]

    context = {
        'posts': random_posts,
    }
    return render(request, 'explore.html', context)


def explore_users(request):
    random_users = get_recommended_users(request)[:40]

    context = {
        'users': random_users,
    }
    return render(request, 'explore_users.html', context)


def profile(request, username=None):
    if not username or request.user.username == username:
        if request.user.is_authenticated:
            user = request.user
            template_name = 'my_profile.html'
        else:
            messages.info(request, 'Войдите в аккаунт, чтобы посмотреть свой профиль')
            return redirect('login')

    else:
        user = User.objects.get(username=username)
        if not user:
            messages.warning(request, f'Аккаунта с @{username} не существует')
            return redirect('index')
        template_name = 'profile.html'

    if request.user.is_authenticated:
        is_following = request.user.profile.following.filter(user=user).exists()
    else:
        is_following = False

    recommended_users = get_recommended_users(request, user.pk)[:6]

    if 'profile-bookmarks' in request.path:
        template_name = 'my_bookmarks.html'
        posts = request.user.profile.bookmarks.filter(is_archived=False)
    else:
        posts = Post.objects.filter(user_profile=user.profile, is_archived=False).order_by('-created')

    context = {
        'person': user,
        'num_of_followers': user.profile.get_number_of_followers(),
        'num_of_following': user.profile.get_number_of_following(),
        'is_following': is_following,
        'posts': posts,
        'recommended_users': recommended_users,
    }
    return render(request, template_name, context)


@login_required
def profile_settings_info(request):
    user = request.user

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)
        profile_form = UpdateProfileForm(request.POST, instance=user.profile, files=request.FILES)

        if request.POST.get('delete_current_photo') == 'Удалить текущее фото':
            user.profile.profile_pic.delete()
            messages.success(request, mark_safe('<i class="fa-regular fa-face-frown"></i> Фото профиля удалено. Давай загрузим новое!'))

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль обновлен!')
            return redirect(to='my-profile')
        else:
            messages.error(request, 'Не удалось обновить профиль. Проверьте правильность введенных данных и повторите попытку.')

    else:
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateProfileForm(instance=user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile_settings.html', context)


def followers(request, username):
    user = User.objects.get(username=username)
    if not user:
        return redirect('index')

    user_profile = user.profile
    users_followers = user_profile.followers.all

    context = {
        'header': 'Подписчики',
        'users_followers': users_followers,
    }

    return render(request, 'follow_list.html', context)


def following(request, username):
    user = User.objects.get(username=username)
    if not user:
        return redirect('index')

    user_profile = user.profile
    users_following = user_profile.following.all

    context = {
        'header': 'Подписки',
        'users_following': users_following,
    }
    return render(request, 'follow_list.html', context)


@login_required
def post_picture(request):
    if request.method == 'POST':
        form = PostPictureForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = Post(
                user_profile=request.user.profile,
                title=form.cleaned_data.get('title'),
                image=request.FILES.get('image'),
            )
            post.save()
            messages.success(request, mark_safe('<i class="fa-regular fa-images me-1"></i> Пост опубликован!'))
            return redirect('index')
        else:
            messages.error(request, mark_safe('<i class="fa-regular fa-face-surprise me-1"></i> Что-то не так. Проверь правильность своего поста!'))
    else:
        form = PostPictureForm()

    context = {
        'form': form,
    }
    return render(request, 'post_create.html', context)


def post(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if not post:
        messages.warning(request, f'Такой публикации не существует или она была удалена')
        return redirect('index')

    if request.user.is_authenticated:
        add_posts_likes(request.user, post)
        is_following = request.user.profile.following.filter(user=post.user_profile.user).exists()
    else:
        is_following = False

    other_posts = Post.objects.filter(user_profile=request.user.profile, is_archived=False).exclude(pk=post.pk)[:6]

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment.objects.create(
                post=post,
                user=request.user,
                comment=comment_form.cleaned_data.get('comment'),
            )
            return redirect('post', post.pk)
        else:
            messages.error(request, 'Не получилось добавить комментарий. Попробуй еще раз.')
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'other_posts': other_posts,
        'comments': post.comment_set.all().order_by('-created'),
        'is_following': is_following,
        'comment_form': comment_form,
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if not post:
        messages.warning(request, f'Такой публикации не существует или она была удалена')
        return redirect('index')

    if request.user.profile != post.user_profile:
        messages.error(request, f'Вы не можете отредактировать эту публикацию')
        return redirect('index')

    if request.method == 'POST':
        form = EditPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post', post.pk)
        else:
            messages.error(request, 'Не получилось отредактировать пост. Попробуй еще раз.')
    else:
        form = EditPostForm(instance=post)

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'post_edit.html', context)


def likes(request, pk):
    post = Post.objects.get(pk=pk)
    if not post:
        return redirect('index')

    likes = Like.objects.filter(post=post)

    context = {
        'header': 'Лайки',
        'likes': likes,
    }
    return render(request, 'follow_list.html', context)
