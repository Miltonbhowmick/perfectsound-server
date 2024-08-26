from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from mutagen import File
from datetime import timedelta
import librosa
import json
import numpy as np


class Artist(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(_("Slug"), max_length=55, unique=True, blank=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Album(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(_("Slug"), max_length=55, unique=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")
    release_date = models.DateField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(_("Slug"), max_length=55, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Track(models.Model):
    title = models.CharField(_("Title"), max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        "common.Category",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="tracks",
    )
    sub_category = models.ForeignKey(
        "common.SubCategory",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="tracks",
    )
    artist = models.ForeignKey(
        Artist, on_delete=models.SET_NULL, related_name="tracks", null=True, blank=True
    )
    album = models.ForeignKey(
        Album, on_delete=models.SET_NULL, related_name="tracks", null=True, blank=True
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, related_name="tracks", null=True, blank=True
    )
    audio_file = models.FileField(upload_to="tracks/")
    duration = models.DurationField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    beats = models.TextField(
        _("Beats"),
        blank=True,
        null=True,
    )
    release_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_duration_in_minutes(self):
        minutes, seconds = divmod(self.duration.total_seconds(), 60)
        return f"{int(minutes)}:{int(seconds)}"

    def save(self, *args, **kwargs):
        if self.audio_file:
            audio = File(self.audio_file)
            if audio and audio.info:
                self.duration = timedelta(seconds=int(audio.info.length))
                self.duration_seconds = audio.info.length
        super().save(*args, **kwargs)

    def generate_beats(self):
        audio_signal, _ = librosa.load(self.audio_file.path, sr=50)
        self.beats = json.dumps(audio_signal.tolist())
        # self.save() // :P :D Its a bomb! recurisve save occurs


@receiver(post_save, sender=Track)
def after_track_save(sender, instance, created, **kwargs):
    if created:
        instance.generate_beats()
        instance.save(update_fields=["beats"])


class Playlist(models.Model):
    title = models.CharField(_("Title"), max_length=255, null=True, blank=True)
    slug = models.SlugField(_("Slug"), max_length=55, unique=True, blank=True)
    track = models.ManyToManyField(Track)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
