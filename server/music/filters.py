import django_filters as filters

from .models import *


class TrackFilter(filters.FilterSet):
    class Meta:
        model = Track
        fields = {"category__slug": ["exact"], "sub_category__slug": ["exact"]}
