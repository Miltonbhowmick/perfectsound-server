# Generated by Django 5.0.8 on 2024-08-31 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_promocode_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='End date'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Start date'),
        ),
    ]
