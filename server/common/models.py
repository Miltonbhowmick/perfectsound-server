from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=255, blank=True, null=True)
    slug = models.SlugField(_("Slug"), max_length=55, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    name = models.CharField(_("Name"), max_length=255, blank=True, null=True)
    slug = models.SlugField(_("Slug"), max_length=55, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="sub_categories",
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Favorite(models.Model):
    user = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="favorites"
    )
    track = models.ForeignKey(
        "music.Track", on_delete=models.CASCADE, related_name="favorites"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "track")

    def __str__(self):
        return f"{self.user} - {self.track}"
