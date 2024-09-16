from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils.choices import OrderStatusChoice


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
    price_plan_credit = models.ForeignKey(
        "payment.PricePlanCredit",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="orders",
    )
    promo_code = models.ForeignKey(
        "payment.PromoCode",
        max_length=255,
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
    status = models.CharField(
        choices=OrderStatusChoice,
        default=OrderStatusChoice.PENDING,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name}-{self.company}"


class Download(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    track = models.ForeignKey("music.Track", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class Transaction(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    track = models.ForeignKey("music.Track", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class UserCredits(models.Model):
    user = models.OneToOneField(
        "account.User", on_delete=models.CASCADE, related_name="credits"
    )
    total_credits = models.PositiveIntegerField(default=0)
    used_credits = models.PositiveIntegerField(default=0)
    remaining_credits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user}-{self.used_credits}"
