# Generated by Django 3.1.3 on 2020-11-14 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
        ('pathway', '0002_displaystage_firm'),
    ]

    operations = [
        migrations.AddField(
            model_name='displaystage',
            name='stage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='questions.stage'),
        ),
    ]
