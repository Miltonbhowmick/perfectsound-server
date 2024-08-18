from rest_framework import serializers

from .models import *
from music.serializers import MinimalTrackSerializer


class MinimalSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = MinimalSubCategorySerializer(
        many=True, read_only=True, source="sub_categories"
    )

    class Meta:
        model = Category
        fields = ["id", "name", "subcategories"]


class FavouriteSerializer(serializers.ModelSerializer):
    track = MinimalTrackSerializer()

    class Meta:
        model = Favorite
        fields = ["id", "track"]
