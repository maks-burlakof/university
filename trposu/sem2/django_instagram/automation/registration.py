# Run this script via terminal: python3 manage.py shell < automation/registration.py

import json
import os
import shutil
from random import randint
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from feeds.models import Profile, Post

with open('automation/users.json', 'r') as f:
    users = json.loads(f.read())

    for user in users:
        user_obj = User(
            username=user['username'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            email=user['email'],
        )
        user_obj.set_password(user['password'])
        user_obj.save()

        user_obj.profile.site_url = user['site_url']
        user_obj.profile.description = user['description']
        user_obj.profile.gender = user['gender']

        os.makedirs(f"media/{user['username']}/")
        shutil.copyfile(
            f"automation/images/{user['profile_pic']}",
            f"media/{user['username']}/{user['profile_pic']}"
        )

        user_obj.profile.profile_pic = user['username'] + '/' + user['profile_pic']
        user_obj.profile.save()

        for post in user['posts']:
            shutil.copyfile(
                f"automation/images/{post['image']}",
                f"media/{user['username']}/{post['image']}"
            )

            post_obj = Post.objects.create(
                user_profile=user_obj.profile,
                group=None,
                title=post['title'],
                image=user['username'] + '/' + post['image'],
                is_allow_comments=post['is_allow_comments'],
            )
            post_obj.created = datetime.now().astimezone() - timedelta(days=randint(1, 30))
            post_obj.save(update_fields=['created'])

        print(f"Finished for @{user['username']}")

users = User.objects.all()
num_of_users = users.count()

for user in users:
    num_of_followers = randint(1, num_of_users)
    followers = Profile.objects.all().order_by('?')[:num_of_followers]

    user.profile.followers.add(*followers)

print("The followers was added successfully!")
