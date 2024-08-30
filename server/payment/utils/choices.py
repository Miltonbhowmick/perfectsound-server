from django.db import models


class DurationChoices(models.TextChoices):
    WEEK = "week", "Week"
    MONTH = "month", "Month"
    ANNUAL = "year", "Year"
    CUSTOM = "custom", "Custom"
