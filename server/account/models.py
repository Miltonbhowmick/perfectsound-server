from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import UserProfileManager
from .utils.choices import *
from .utils.utils import generate_otp
from .emails import send_otp_email, newsletter_email


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("Username"), max_length=100, unique=True)
    email = models.EmailField(_("Email"), max_length=100, unique=True)
    first_name = models.CharField(
        _("First Name"), max_length=255, blank=True, null=True
    )
    last_name = models.CharField(_("Last Name"), max_length=255, blank=True, null=True)
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

    is_email_verified = models.BooleanField(_("Is email verified?"), default=False)
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

    def send_verification_code(self, reason=None, email=None):
        if email:
            obj, created = Verification.objects.get_or_create(email=email)
            if not created:
                obj.code = generate_otp()
                obj.save()
            send_otp_email(email=email, otp=obj.code, reason=reason)


class Verification(models.Model):
    email = models.EmailField(_("Email"), max_length=100)
    code = models.IntegerField(_("Code"), default=generate_otp, null=True, blank=True)

    def __str__(self):
        return str(self.email)


class Newsletter(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    attachments = models.FileField(upload_to="newsletters/", null=True, blank=True)

    def __str__(self):
        return self.email

    def send_newsletter(self):
        if self.email:
            if self.attachments:
                newsletter_email(
                    self.email, self.name, self.description, self.attachments
                )
            else:
                newsletter_email(self.email, self.name, self.description)


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="subscriptions",
    )
    order = models.OneToOneField(
        "order.Order",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
