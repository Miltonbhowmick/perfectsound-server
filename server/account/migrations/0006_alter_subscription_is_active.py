# Generated by Django 5.0.8 on 2024-09-09 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_subscription_created_at_subscription_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
