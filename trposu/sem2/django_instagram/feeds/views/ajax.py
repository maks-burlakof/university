from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

from feeds.models import Profile, Post, Like, Comment


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


@login_required
def bookmark(request):
    post_pk = request.GET.get('post')
    action = request.GET.get('action')
    is_success = False
    message = ""
    try:
        post = Post.objects.get(pk=post_pk)
        if action == "add":
            request.user.profile.bookmarks.add(post)
            is_success = True
        elif action == "remove":
            request.user.profile.bookmarks.remove(post)
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
def comment_delete(request):
    comment_pk = request.GET.get('comment')
    is_success = False
    message = ""

    try:
        comment = Comment.objects.get(pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
            is_success = True
        else:
            message = "This comment is not yours"
    except Exception as e:
        message = str(e)

    response = {
        'is_success': is_success,
        'message': message,
    }
    return JsonResponse(response)


def qr_code_generator(request):
    import qrcode
    from PIL import Image
    from io import BytesIO
    import base64

    qr_text = request.GET.get('text')
    qr_image = qrcode.make(qr_text, box_size=15)
    qr_image_pil = qr_image.get_image()

    stream = BytesIO()
    qr_image_pil.save(stream, format='PNG')
    qr_image_data = stream.getvalue()
    qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')

    response = {
        'is_success': True,
        'qr_image_base64': qr_image_base64,
    }
    return JsonResponse(response)
