from django.db import models


class DurationChoices(models.TextChoices):
    WEEK = "week", "Week"
    MONTH = "month", "Month"
    ANNUAL = "year", "Year"
    CUSTOM = "custom", "Custom"


class PaymentMethodTypeChoices(models.TextChoices):
    STRIPE = "stripe", "Stripe"
    PAYPAL = "paypal", "Paypal"
