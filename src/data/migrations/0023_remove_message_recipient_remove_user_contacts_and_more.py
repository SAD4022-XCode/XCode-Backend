# Generated by Django 5.0.4 on 2024-07-02 20:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0022_message_recipient_user_contacts_alter_message_sender"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="message",
            name="recipient",
        ),
        migrations.RemoveField(
            model_name="user",
            name="contacts",
        ),
        migrations.AlterField(
            model_name="message",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]