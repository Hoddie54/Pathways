# Generated by Django 3.1.3 on 2020-11-16 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathway', '0004_pathwaypoint_userpathwaypoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpathwaypoint',
            name='rating',
            field=models.IntegerField(default=1),
        ),
    ]
