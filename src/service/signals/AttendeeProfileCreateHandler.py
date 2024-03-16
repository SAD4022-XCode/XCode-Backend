from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from data.models import AttendeeProfile

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def AttendeeProfileCreateHandler(sender, instance, created, **kwargs):
    if not created:
        return
    profile = AttendeeProfile(user = instance)
    profile.save()