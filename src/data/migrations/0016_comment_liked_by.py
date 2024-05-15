# Generated by Django 5.0.4 on 2024-05-15 15:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0015_alter_comment_score"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="liked_by",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
