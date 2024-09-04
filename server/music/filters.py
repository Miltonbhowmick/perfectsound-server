import django_filters as filters

from .models import *


class TrackFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Track
        fields = {
            "category__slug": ["exact"],
            "sub_category__slug": ["exact"],
        }
