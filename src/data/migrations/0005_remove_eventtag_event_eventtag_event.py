# Generated by Django 5.0.4 on 2024-04-26 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0004_remove_taggedevent_tag_remove_taggedevent_event_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="eventtag",
            name="event",
        ),
        migrations.AddField(
            model_name="eventtag",
            name="event",
            field=models.ManyToManyField(to="data.event"),
        ),
    ]
