import os
import logging
from django.db.models.signals import post_save, pre_delete, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile, Post, Group

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


def delete_directory_if_empty(directory_path):
    """
        Currently not in use.
    """
    if not os.listdir(directory_path):
        last_folder = os.path.basename(directory_path)
        if last_folder.strip('/') != 'media':
            result = os.system("rm -r {}".format(directory_path))
            if result != 0:
                logger.error('Error when deleting the image directory {}.'.format(directory_path))


@receiver(pre_delete, sender=Profile)
@receiver(pre_delete, sender=Group)
def delete_profile_pic(sender, instance, **kwargs):
    if instance.profile_pic:
        filepath = instance.profile_pic.path
        if os.path.isfile(filepath):
            os.remove(filepath)
        directory_path = os.path.dirname(filepath)
        delete_directory_if_empty(directory_path)


@receiver(pre_delete, sender=Post)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        filepath = instance.image.path
        if os.path.isfile(filepath):
            os.remove(filepath)
        directory_path = os.path.dirname(filepath)
        delete_directory_if_empty(directory_path)


@receiver(pre_save, sender=Profile)
def update_image(sender, instance, **kwargs):
    if not instance.pk:
        instance.is_update_image = False
        return False
    try:
        old_image = sender.objects.get(pk=instance.pk).profile_pic
    except sender.DoesNotExist:
        return False
    is_new = old_image != instance.profile_pic
    if is_new:
        instance.is_update_image = True
        if old_image and os.path.isfile(old_image.path):
            os.remove(old_image.path)
