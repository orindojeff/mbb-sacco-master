from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile

User: AbstractUser = get_user_model()


@receiver(post_save, sender=User, dispatch_uid="creating_user_profile")
def creating_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
