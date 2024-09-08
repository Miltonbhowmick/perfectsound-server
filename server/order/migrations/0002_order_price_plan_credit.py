# Generated by Django 5.0.8 on 2024-09-08 05:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        ('payment', '0009_promocode_end_date_promocode_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price_plan_credit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='payment.priceplancredit'),
        ),
    ]
