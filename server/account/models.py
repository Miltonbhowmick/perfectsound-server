from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import UserProfileManager
from .utils.choices import *


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("Username"), max_length=100, unique=True)
    email = models.EmailField(_("Email"), max_length=100, unique=True)
    first_name = models.CharField(
        _("First Name"), max_length=255, blank=True, null=True
    )
    last_name = models.CharField(_("Last Name"), max_length=255, blank=True, null=True)
    is_email_verified = models.BooleanField(_("Is email verified?"), default=False)
    mobile_number = models.CharField(
        _("Mobile number"), max_length=50, null=True, blank=True
    )
    gender = models.IntegerField(
        _("Gender"),
        choices=GenderChoice.choices,
        default=GenderChoice.MALE,
        null=True,
        blank=True,
    )
    address = models.CharField(
        _("Permanent address"), max_length=250, null=True, blank=True
    )
    city = models.CharField(_("City"), max_length=150, null=True, blank=True)
    post_code = models.CharField(_("Post code"), max_length=100, null=True, blank=True)
    country = models.CharField(_("Country"), max_length=100, null=True, blank=True)

    join_date = models.DateTimeField(
        _("Join date"), auto_now_add=True, null=True, blank=True
    )

    is_active = models.BooleanField(_("Is active"), default=True)
    is_staff = models.BooleanField(_("Is staff"), default=False)
    is_2fa = models.BooleanField(_("Is 2FA?"), default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    def __str__(self):
        if self.username:
            return self.username
        else:
            return self.email.split("@")[0]

    class Meta:
        ordering = ("-join_date",)
