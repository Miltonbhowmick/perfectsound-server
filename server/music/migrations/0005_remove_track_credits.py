# Generated by Django 5.0.8 on 2024-09-15 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_track_credits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='credits',
        ),
    ]
