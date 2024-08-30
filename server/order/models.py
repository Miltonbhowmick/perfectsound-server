from django.db import models
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    user = models.ForeignKey(
        "account.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    first_name = models.CharField(
        _("First Name"), max_length=255, null=True, blank=True
    )
    last_name = models.CharField(_("Last Name"), max_length=255, null=True, blank=True)
    phone_number = models.CharField(
        _("Phone Number"), max_length=100, null=True, blank=True
    )
    price_plan = models.ForeignKey(
        "payment.PricePlan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    promo_code = models.ForeignKey(
        "payment.PromoCode",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    company = models.CharField(_("Company"), max_length=255, null=True, blank=True)
    address1 = models.TextField(_("Address 1"), max_length=255, null=True, blank=True)
    address2 = models.TextField(_("Address 2"), max_length=255, null=True, blank=True)
    country = models.CharField(_("Country"), max_length=255, null=True, blank=True)
    city = models.CharField(_("City"), max_length=255, null=True, blank=True)
    state = models.TextField(_("State"), max_length=255, null=True, blank=True)
    zip_code = models.TextField(_("Zip Code"), max_length=255, null=True, blank=True)
    is_agreed_policy = models.BooleanField(_("Is Agreed Policy"), default=False)

    def __str__(self):
        return self.first_name
