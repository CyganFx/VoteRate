# Generated by Django 3.2 on 2021-05-28 13:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0010_pollreports_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollreports',
            name='at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]