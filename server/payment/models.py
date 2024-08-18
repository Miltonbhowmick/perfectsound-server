from django.db import models

from .utils.choices import *


class PricePlanCredit(models.Model):
    credit = models.IntegerField(default=0, null=True, blank=True)
    amount = models.DecimalField(
        default=0, decimal_places=4, max_digits=12, null=True, blank=True
    )

    def __str__(self):
        return self.id


class PricePlan(models.Model):
    duration = models.CharField(choices=DurationChoices, blank=True, null=True)
    duration_unit = models.IntegerField(default=0, null=True, blank=True)
    description = models.TextField(max_length=755, null=True, blank=True)
    amount = models.DecimalField(
        default=0, decimal_places=4, max_digits=12, null=True, blank=True
    )
    credit = models.ManyToManyField(PricePlanCredit, related_name="priceplans")

    def __str__(self):
        return self.duration
