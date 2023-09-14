from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from feeds.models import Profile, Post, Like
from feeds.forms import UpdateProfileForm, UpdateUserForm, PostPictureForm


def index(request):
    if request.user.is_authenticated:
        user = request.user
        users_followed = request.user.profile.following.all()
        posts = Post.objects.filter(
            Q(user_profile__in=users_followed) |
            Q(user_profile=user.profile),
            is_archived=False,
        ).select_related('user_profile', 'user_profile__user').order_by('-created')
    else:
        # TODO: show random posts
        return redirect('login')

    context = {
        'posts': posts,
    }

    return render(request, 'index.html', context)


def explore(request):
    random_posts = Post.objects.all().order_by('?')[:40]

    context = {
        'posts': random_posts
    }
    return render(request, 'explore.html', context)


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

    context = {
        'person': user,
        'num_of_followers': user.profile.get_number_of_followers(),
        'num_of_following': user.profile.get_number_of_following(),
        'posts': Post.objects.filter(user_profile=user.profile, is_archived=False),
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


def post(request, pk):
    post = Post.objects.get(pk=pk)
    if not post:
        return redirect('index')

    liked = Like.objects.filter(post=post, user=request.user).exists()

    context = {
        'post': post,
        'liked': liked,
    }
    return render(request, 'post.html', context)


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
