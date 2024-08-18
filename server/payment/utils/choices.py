from django.db import models


class DurationChoices(models.IntegerChoices):
    MONTH = 0, "Month"
    SIX_MONTH = 1, "Six Month"
    ANNUAL = 2, "Annual"
    CUSTOM = 3, "Custom"
