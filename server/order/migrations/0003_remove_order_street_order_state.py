# Generated by Django 5.0.8 on 2024-08-30 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_zip_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='street',
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='State'),
        ),
    ]
