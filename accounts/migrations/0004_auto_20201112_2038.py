# Generated by Django 3.1.3 on 2020-11-12 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20201111_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='university_society',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='year',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='university',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
