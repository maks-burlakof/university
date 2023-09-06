from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from feeds.models import UserProfile, Post
from feeds.forms import UpdateProfileForm, UpdateUserForm


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    users_followed = request.user.userprofile.following.all()
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

    user_profile = UserProfile.objects.get(user=user)

    context = {
        'user': user,
        'profile': user_profile,
    }
    return render(request, 'profile.html', context)


def my_profile(request):
    user = request.user
    user_profile = user.userprofile

    context = {
        'user': user,
        'profile': user_profile,
    }
    return render(request, 'my_profile.html', context)


@login_required
def profile_settings(request):
    user = request.user

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)
        profile_form = UpdateProfileForm(request.POST, instance=user.userprofile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Изменения сохранены!')
            return redirect(to='my-profile')
    else:
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateProfileForm(instance=user.userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile_settings.html', context)


def followers(request, username):
    user = User.objects.get(username=username)
    if not user:
        return redirect('index')

    user_profile = user.userprofile
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

    user_profile = user.userprofile
    users_following = user_profile.following.all

    context = {
        'header': 'Подписки',
        'users_following': users_following,
    }
    return render(request, 'follow_list.html', context)


@login_required
def post_picture(request):
    pass


