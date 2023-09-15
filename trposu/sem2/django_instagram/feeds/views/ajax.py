from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

from feeds.models import Profile, Post, Like


def validate_username(request):
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


@login_required
def like(request):
    post_pk = request.GET.get('post')
    action = request.GET.get('action')
    is_success = False
    message = ""
    try:
        post = Post.objects.get(pk=post_pk)
        if action == "add":
            like = Like(post=post, user=request.user)
            like.save()
            is_success = True
        elif action == "remove":
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            is_success = True
        else:
            message = "Action is not provided"
    except Exception as e:
        message = str(e)

    response = {
        'is_success': is_success,
        'message': message,
    }
    return JsonResponse(response)


@login_required
def follow(request):
    action = request.GET.get('action')
    follow_profile_pk = request.GET.get('user')
    is_success = False
    message = ""

    user_profile = request.user.profile
    follow_profile = User.objects.get(pk=follow_profile_pk).profile

    if user_profile != follow_profile:
        try:
            if action == 'follow':
                user_profile.following.add(follow_profile)
                follow_profile.followers.add(user_profile)
                is_success = True
            elif action == 'unfollow':
                user_profile.following.remove(follow_profile)
                follow_profile.followers.remove(user_profile)
                is_success = True
            else:
                message = "Action is not provided"
        except Exception as e:
            message = str(e)
    else:
        message = "You can't follow yourself"

    response = {
        'is_success': is_success,
        'message': message,
    }
    return JsonResponse(response)
