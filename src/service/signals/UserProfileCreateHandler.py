from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from data.models import UserProfile

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def UserProfileCreateHandler(sender, instance, created, **kwargs):
    if not created:
        return
    profile = UserProfile(user = instance)
    profile.save()