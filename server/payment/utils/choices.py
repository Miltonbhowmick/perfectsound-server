from django.db import models


class DurationChoices(models.TextChoices):
    MONTH = "month", "Month"
    SIX_MONTH = "six_month", "Six Month"
    ANNUAL = "annual", "Annual"
    CUSTOM = "custom", "Custom"
