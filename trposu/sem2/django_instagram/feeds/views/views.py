from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe

from feeds.models import Profile, Post, Like, Comment, Group
from feeds.forms import (UpdateProfileForm, UpdateUserForm, PostPictureForm, CommentForm, EditPostForm,
                         GroupCreateForm, GroupEditForm)

POSTS_ON_PAGE = 30

POST_SR = ['user_profile', 'user_profile__user', 'group', 'group__owner']
POST_PR = ['likes', 'comments']
COMMENT_SR = ['user', 'user__profile']
GROUP_SR = ['owner']


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


def get_recommended_groups(group_exclude=None):
    id_list = []
    if group_exclude:
        id_list.append(group_exclude.pk)
    return Group.objects.all().exclude(pk__in=id_list).select_related(*GROUP_SR).order_by('?')


def index(request):
    if request.user.is_authenticated:
        user = request.user
        users_following, group_following = request.user.profile.get_following_users_groups()
        posts = Post.objects.filter(
            Q(user_profile__user__in=users_following) |
            Q(user_profile=user.profile) |
            Q(group__in=group_following),
            is_archived=False,
        ).select_related(*POST_SR).prefetch_related(*POST_PR).order_by('-created')[:POSTS_ON_PAGE]
        add_posts_likes(user, posts)
        owned_groups = Group.objects.filter(owner=request.user)
    else:
        posts = Post.objects.filter(is_archived=False).select_related('user_profile', 'user_profile__user').order_by('?')[:POSTS_ON_PAGE]
        owned_groups = None

    recommended_users = get_recommended_users(request)[:5]

    context = {
        'posts': posts,
        'owned_groups': owned_groups,
        'recommended_users': recommended_users,
    }

    return render(request, 'index.html', context)


def explore(request):
    random_posts = Post.objects.filter(is_archived=False).select_related(*POST_SR).prefetch_related(*POST_PR).order_by('?')[:40]

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


def explore_groups(request):
    context = {
        'recommended_groups': get_recommended_groups(),
    }
    return render(request, 'explore_groups.html', context)


def search(request):
    search_text = request.GET.get('q', '')
    search_users = request.GET.get('users', '')
    search_groups = request.GET.get('groups', '')
    search_posts = request.GET.get('posts', '')

    if search_users:
        users_result = User.objects.filter(
            Q(username__contains=search_text) |
            Q(first_name__contains=search_text) |
            Q(last_name__contains=search_text) |
            Q(profile__site_url__contains=search_text) |
            Q(profile__description__contains=search_text),
        ).select_related('profile').order_by('-id')
    else:
        users_result = None

    if search_groups:
        groups_result = Group.objects.filter(
            Q(title__contains=search_text) |
            Q(groupname__contains=search_text) |
            Q(site_url__contains=search_text) |
            Q(description__contains=search_text),
        ).select_related(*GROUP_SR).order_by('-id')
    else:
        groups_result = None

    if search_posts:
        posts_result = Post.objects.filter(
            Q(title__contains=search_text) |
            Q(created__contains=search_text) |
            Q(group__groupname__contains=search_text) |
            Q(group__title__contains=search_text) |
            Q(user_profile__user__username__contains=search_text) |
            Q(user_profile__user__first_name__contains=search_text) |
            Q(user_profile__user__last_name__contains=search_text),
            is_archived=False,
        ).select_related(*POST_SR).prefetch_related(*POST_PR).order_by('-created')
    else:
        posts_result = None

    if not search_text:
        users_result = None
        groups_result = None
        posts_result = None

    context = {
        'search_text': search_text,
        'search_users': search_users,
        'search_groups': search_groups,
        'search_posts': search_posts,
        'users_result': users_result,
        'groups_result': groups_result,
        'posts_result': posts_result,
    }
    return render(request, 'search_results.html', context)


def profile(request, username=None):
    if not username or request.user.username == username:
        if request.user.is_authenticated:
            user = request.user
            template_name = 'my_profile.html'
        else:
            messages.info(request, 'Войдите в аккаунт, чтобы посмотреть свой профиль')
            return redirect('login')

    else:
        user = get_object_or_404(User.objects.select_related('profile'), username=username)
        template_name = 'profile.html'

    if request.user.is_authenticated:
        is_following = user.profile.followers.filter(user=request.user).exists()
    else:
        is_following = False

    recommended_users = get_recommended_users(request, user.pk)[:6]

    if 'profile-bookmarks' in request.path:
        template_name = 'my_bookmarks.html'
        posts = request.user.profile.bookmarks.filter(is_archived=False).select_related(*POST_SR).prefetch_related(*POST_PR)
    elif 'profile-archived' in request.path:
        template_name = 'my_archived.html'
        posts = Post.objects.filter(user_profile=request.user.profile, is_archived=True).select_related(*POST_SR).prefetch_related(*POST_PR).order_by('-created')
    else:
        posts = Post.objects.filter(user_profile=user.profile, is_archived=False).select_related(*POST_SR).prefetch_related(*POST_PR).order_by('-created')

    users_following, groups_following = user.profile.get_following_users_groups()
    followers = user.profile.followers.all().select_related('user')

    context = {
        'person': user,
        'followers': followers,
        'users_following': users_following,
        'groups_following': groups_following,
        'num_of_following': users_following.count() + groups_following.count(),
        'is_following': is_following,
        'posts': posts,
        'recommended_users': recommended_users,
    }
    return render(request, template_name, context)


def group(request, groupname):
    group = get_object_or_404(Group.objects.select_related(*GROUP_SR), groupname=groupname)

    if request.user == group.owner:
        template_name = 'my_group.html'
    else:
        template_name = 'group.html'

    if request.user.is_authenticated:
        is_following = group.followers.filter(pk=request.user.profile.pk).exists()
    else:
        is_following = False

    if group.owner == request.user and 'group-archived' in request.path:
        template_name = 'my_group_archived.html'
        posts = Post.objects.filter(group=group, is_archived=True).select_related(*POST_SR).prefetch_related(*POST_PR).order_by('-created')
    else:
        posts = Post.objects.filter(group=group, is_archived=False).select_related(*POST_SR).prefetch_related(*POST_PR).order_by('-created')

    context = {
        'group': group,
        'followers': group.followers.all().select_related('user'),
        'is_following': is_following,
        'posts': posts,
        'recommended_groups': get_recommended_groups(group_exclude=group),
    }
    return render(request, template_name, context)


@login_required
def group_create(request):
    if request.method == 'POST':
        form = GroupCreateForm(request.POST, files=request.FILES)
        if form.is_valid():
            group = Group.objects.create(
                groupname=form.cleaned_data.get('groupname'),
                owner=request.user,
                title=form.cleaned_data.get('title'),
                profile_pic=request.FILES.get('profile_pic'),
                description=form.cleaned_data.get('description'),
                site_url=form.cleaned_data.get('site_url'),
            )
            group.followers.add(request.user.profile)
            messages.success(request, 'Сообщество создано!')
            return redirect('group', group.groupname)
        else:
            messages.error(request, 'Не получилось. Проверьте правильность введенных данных и повторите попытку.')

    else:
        form = GroupCreateForm()

    context = {
        'form': form,
    }
    return render(request, 'group_create.html', context)


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


@login_required
def group_settings(request, groupname):
    group = get_object_or_404(Group, groupname=groupname)
    if group.owner != request.user:
        messages.error(request, "Вы не можете редактировать настройки этой группы")
        return redirect('group', groupname)

    if request.method == 'POST':
        form = GroupEditForm(request.POST, instance=group, files=request.FILES)

        if request.POST.get('delete_current_photo') == 'Удалить текущее фото':
            group.profile_pic.delete()
            messages.success(request, mark_safe('<i class="fa-regular fa-face-frown"></i> Главное фото удалено. Давай загрузим новое!'))

        if form.is_valid():
            form.save()
            messages.success(request, 'Сообщество обновлено!')
            return redirect('group', groupname)
        else:
            messages.error(request, 'Не удалось изменить настройки. Проверьте правильность введенных данных и повторите попытку.')

    else:
        form = GroupEditForm(instance=group)

    context = {
        'form': form,
        'group': group,
    }
    return render(request, 'group_settings.html', context)


@login_required
def post_picture(request):
    user_owned_groups = Group.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = PostPictureForm(data=request.POST, files=request.FILES)
        if form.is_valid():

            from_account = request.POST.get('from_account')
            print(from_account)
            if from_account == request.user.username:
                post_user_profile = request.user.profile
                post_group = None
            else:
                post_group = user_owned_groups.get(groupname=from_account)
                if not post_group:
                    messages.error(request, f'Не удалось найти аккаунт @{from_account} для публикации')
                    return redirect('post-create')
                post_user_profile = None

            post = Post(
                user_profile=post_user_profile,
                group=post_group,
                title=form.cleaned_data.get('title'),
                image=request.FILES.get('image'),
                is_allow_comments=form.cleaned_data.get('is_allow_comments'),
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
        'user_owned_groups': user_owned_groups,
    }
    return render(request, 'post_create.html', context)


def post(request, post_pk):
    post = get_object_or_404(Post.objects.select_related(*POST_SR).prefetch_related(*POST_PR), pk=post_pk)

    if post.user_profile:
        if request.user.is_authenticated:
            add_posts_likes(request.user, post)
            is_following = post.user_profile.followers.filter(user=request.user).exists()
        else:
            is_following = False
        other_posts = Post.objects.filter(user_profile=post.user_profile, is_archived=False).exclude(pk=post.pk).select_related(*POST_SR).prefetch_related(*POST_PR)[:6]
        template_name = 'post.html'

    else:
        if request.user.is_authenticated:
            add_posts_likes(request.user, post)
            is_following = post.group.followers.filter(user=request.user).exists()
        else:
            is_following = False
        other_posts = Post.objects.filter(group=post.group, is_archived=False).exclude(pk=post.pk).select_related(*POST_SR).prefetch_related(*POST_PR)[:6]
        template_name = 'post_from_group.html'

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
        'comments': post.comments.all().select_related(*COMMENT_SR).order_by('-created'),
        'is_following': is_following,
        'comment_form': comment_form,
    }
    return render(request, template_name, context)


@login_required
def post_edit(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if not post:
        messages.warning(request, f'Такой публикации не существует или она была удалена')
        return redirect('index')

    if post.user_profile and request.user.profile == post.user_profile:
        template_name = 'post_edit.html'
    elif post.group and request.user == post.group.owner:
        template_name = 'post_edit_from_group.html'
    else:
        messages.error(request, f'Вы не можете отредактировать эту публикацию')
        return redirect('post', post.pk)

    if request.method == 'POST':
        form = EditPostForm(request.POST, instance=post)

        if request.POST.get('delete_post') == 'Удалить публикацию':
            post.delete()
            messages.success(request, mark_safe('<i class="fa-regular fa-face-frown"></i> Публикация удалена. Давай загрузим новую!'))
            return redirect('index')

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
    return render(request, template_name, context)
