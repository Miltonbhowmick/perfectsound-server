from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils.choices import *


class PromoCode(models.Model):
    title = models.CharField(_("Title"), max_length=255, null=True, blank=True)
    is_active = models.BooleanField(_("Is active"), default=False)

    def __str__(self):
        return self.title


class PricePlanCredit(models.Model):
    credit = models.IntegerField(_("Credit Value"), default=0, null=True, blank=True)
    amount = models.DecimalField(
        _("Amount"), default=0, decimal_places=4, max_digits=12, null=True, blank=True
    )

    def __str__(self):
        return f"{self.credit}-{self.amount}"


class PricePlan(models.Model):
    order = models.IntegerField(_("Serial Order"), default=1, blank=True, null=True)
    duration = models.CharField(
        _("Duration"),
        choices=DurationChoices,
        default=DurationChoices.MONTH,
        blank=True,
        null=True,
    )
    duration_unit = models.IntegerField(
        _("Duration Unit"), default=0, null=True, blank=True
    )
    description = models.TextField(
        _("Description"), max_length=755, null=True, blank=True
    )
    amount = models.DecimalField(
        _("Plan Amount"),
        default=0,
        decimal_places=4,
        max_digits=12,
        null=True,
        blank=True,
    )
    credit = models.ManyToManyField(PricePlanCredit, blank=True)

    def __str__(self):
        return self.duration
