# Generated by Django 5.0.4 on 2024-05-11 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0009_rename_eventtag_tag"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="ticket_price",
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name="inpersonevent",
            name="location_lat",
            field=models.DecimalField(decimal_places=20, max_digits=22),
        ),
        migrations.AlterField(
            model_name="inpersonevent",
            name="location_lon",
            field=models.DecimalField(decimal_places=20, max_digits=22),
        ),
    ]
