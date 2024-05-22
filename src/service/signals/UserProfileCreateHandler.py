from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from data.models import UserProfile

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def user_profile_create_handler(sender, instance, created, **kwargs):
    if not created:
        return
    UserProfile.objects.create(user = instance)