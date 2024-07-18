from django.contrib.auth.models import Group


def check_groups_available():
    admin_group = None
    user_group = None

    try:
        admin_group = Group.objects.get(name='admin')
        print('admin group already exists')

    except Group.DoesNotExist:
        admin_group = Group.objects.create(name='admin')
        print('admin group created')

    try:
        user_group = Group.objects.get(name='user')
        print('user group already exists')

    except Group.DoesNotExist:
        user_group = Group.objects.create(name='user')
        print('user group created')


############### Grant user default group

from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def grant_user_default_group(sender, instance, created, **kwargs):
    if created:
        user_group = Group.objects.get(name='user')
        instance.groups.add(user_group)
        instance.save()
