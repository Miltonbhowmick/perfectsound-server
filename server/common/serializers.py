from rest_framework import serializers

from .models import *
from music.models import Track
from music.serializers import MinimalTrackSerializer


class MinimalSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name"]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    # subcategories = MinimalSubCategorySerializer(
    #     many=True, read_only=True, source="sub_categories"
    # )

    class Meta:
        model = Category
        # fields = ["id", "name", "subcategories"]
        fields = ["id", "name", "slug"]


class FavouriteSerializer(serializers.ModelSerializer):
    track = MinimalTrackSerializer()

    class Meta:
        model = Favorite
        fields = ["id", "track"]


class FavouriteTrackCreateSerializer(serializers.Serializer):
    track = serializers.IntegerField()

    def validate_track(self, value):
        user = self.context["user"]
        if value:
            if not Track.objects.filter(id=value).exists():
                raise serializers.ValidationError(
                    {"track": "This track is not available now."}
                )
            if Favorite.objects.filter(user=user, track_id=value).exists():
                raise serializers.ValidationError(
                    {"track": "This track is already in favourite list."}
                )
        return value

    def create(self, validated_data):
        track = validated_data.get("track")
        user = self.context["user"]
        track_obj = Track.objects.get(id=track)
        new_favorite = Favorite.objects.create(user=user, track=track_obj)
        return new_favorite
