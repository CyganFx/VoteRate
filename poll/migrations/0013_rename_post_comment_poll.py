# Generated by Django 3.2 on 2021-06-04 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0012_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='poll',
        ),
    ]
