# Generated by Django 5.0.8 on 2024-08-30 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='zip_code',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Zip Code'),
        ),
    ]
