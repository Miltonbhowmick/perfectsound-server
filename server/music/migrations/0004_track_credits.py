# Generated by Django 5.0.8 on 2024-09-15 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_track_duration_seconds'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='credits',
            field=models.SmallIntegerField(blank=True, default=3, null=True),
        ),
    ]
