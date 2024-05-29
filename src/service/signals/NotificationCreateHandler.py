# from django.dispatch import receiver
# from django.db.models.signals import post_save

# from data import models

# class PrivateMessage:
#     pass

# @receiver(post_save, sender = PrivateMessage)
# def new_private_message_notification(sender, instance, created, **kwargs):
#     if not created:
#         return
#     models.Notification.objects.create(recipient_id = sender.recipient_id,
#                                        title = "new message",
#                                        content = f"you have a new message from {sender.sender_id}")    
