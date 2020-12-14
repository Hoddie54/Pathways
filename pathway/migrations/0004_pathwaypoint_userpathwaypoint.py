# Generated by Django 3.1.3 on 2020-11-16 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pathway', '0003_displaystage_stage'),
    ]

    operations = [
        migrations.CreateModel(
            name='PathwayPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.TextField()),
                ('displayStage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pathway.displaystage')),
            ],
        ),
        migrations.CreateModel(
            name='UserPathwayPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pathwayPoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pathway.pathwaypoint')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]