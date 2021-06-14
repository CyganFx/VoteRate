# Generated by Django 3.2 on 2021-05-28 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0008_auto_20210521_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='reportCounter',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='PollReports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_type', models.TextField(max_length=50)),
                ('report_text', models.TextField(max_length=200)),
                ('poll_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.poll')),
            ],
        ),
    ]