from rest_framework import serializers

from .models import *


class MinimalTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = [
            "id",
            "title",
            "audio_file",
            "duration",
            "beats",
            "release_date",
            "created_at",
            "updated_at",
        ]


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = "__all__"


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"
