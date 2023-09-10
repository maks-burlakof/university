from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from feeds.models import Profile, Post, Like
from feeds.forms import UpdateProfileForm, UpdateUserForm, PostPictureForm


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    users_followed = request.user.profile.following.all()
    posts = Post.objects.filter(user_profile__in=users_followed).order_by('-created')

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


def profile(request, username):
    user = User.objects.get(username=username)
    if not user:
        return redirect('index')

    user_profile = Profile.objects.get(user=user)

    context = {
        'person': user,
        'person_profile': user_profile,
    }
    return render(request, 'profile.html', context)


@login_required
def my_profile(request):
    user = request.user
    user_profile = user.profile

    context = {
        'person': user,
        'person_profile': user_profile,
    }
    return render(request, 'my_profile.html', context)


@login_required
def profile_settings(request):
    user = request.user

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)
        profile_form = UpdateProfileForm(request.POST, instance=user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Изменения сохранены!')
            return redirect(to='my-profile')
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
            return redirect('my-profile')
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
