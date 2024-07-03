from django.dispatch import receiver
from django.db.models.signals import post_save

from data import models

@receiver(post_save, sender = models.Message, weak = False)
def new_message_notification(sender, instance, created, **kwargs):
    if not created:
        return

    message_sender_name = models.UserPofile.objects \
        .select_related("user") \
        .filter(user_id = instance.sender_id) \
        .first() \
        .user.first_name

    recipients = models.Conversation.objects \
        .prefetch_related("participants") \
        .get(pk = instance.conversation_id) \
        .participants \
        .exclude(id = instance.sender_id) \
        .all()

    notifications = [
        models.Notification(recipient_id = recipient.id,
                                           title = f"New message from {message_sender_name}",
                                           content = instance.content)
        for recipient in recipients    
    ]        

    models.Notification.objects.bulk_create(notifications)
