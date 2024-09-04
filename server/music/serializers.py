from rest_framework import serializers

from .models import *
from common.models import Favorite


class MinimalTrackSerializer(serializers.ModelSerializer):
    beats = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = [
            "id",
            "title",
            "audio_file",
            "duration_seconds",
            "beats",
            "release_date",
            "created_at",
            "updated_at",
            "is_favorite",
        ]

    def get_beats(self, obj):
        """
        Method to convert the JSON string stored in the `beats` field
        back into a Python list (array format).
        """
        if obj.beats:
            try:
                # Attempt to parse the JSON string to a Python list
                return json.loads(obj.beats)
            except (json.JSONDecodeError, TypeError):
                # If there's an error in parsing, return an empty list or handle as needed
                return []
        return []

    def get_is_favorite(self, obj):
        """
        Method to get this track is favorite listed of the request user.
        """
        user = self.context.get("user", None)
        if user and user.is_authenticated:
            return Favorite.objects.filter(user=user, track=obj).exists()
        return False


class MinimalFavouriteTrackSerializer(serializers.ModelSerializer):
    beats = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = [
            "id",
            "title",
            "audio_file",
            "duration_seconds",
            "beats",
            "release_date",
            "created_at",
            "updated_at",
        ]

    def get_beats(self, obj):
        """
        Method to convert the JSON string stored in the `beats` field
        back into a Python list (array format).
        """
        if obj.beats:
            try:
                # Attempt to parse the JSON string to a Python list
                return json.loads(obj.beats)
            except (json.JSONDecodeError, TypeError):
                # If there's an error in parsing, return an empty list or handle as needed
                return []
        return []


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
