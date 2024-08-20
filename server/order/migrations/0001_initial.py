# Generated by Django 5.0.8 on 2024-08-19 15:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payment', '0002_promocode_alter_priceplan_amount_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Last Name')),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Phone Number')),
                ('company', models.CharField(blank=True, max_length=255, null=True, verbose_name='Company')),
                ('address1', models.TextField(blank=True, max_length=255, null=True, verbose_name='Address 1')),
                ('address2', models.TextField(blank=True, max_length=255, null=True, verbose_name='Address 2')),
                ('country', models.CharField(blank=True, max_length=255, null=True, verbose_name='Country')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='City')),
                ('street', models.TextField(blank=True, max_length=255, null=True, verbose_name='Street')),
                ('is_agreed_policy', models.BooleanField(default=False, verbose_name='Is Agreed Policy')),
                ('price_plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='payment.priceplan')),
                ('promo_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='payment.promocode')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
