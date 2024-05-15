# Generated by Django 5.0.4 on 2024-04-26 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0003_event_tag_inpersonevent_onlineevent_taggedevent"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="taggedevent",
            name="tag",
        ),
        migrations.RemoveField(
            model_name="taggedevent",
            name="event",
        ),
        migrations.CreateModel(
            name="EventTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tag", models.CharField(max_length=255)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="data.event"
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Tag",
        ),
        migrations.DeleteModel(
            name="TaggedEvent",
        ),
    ]