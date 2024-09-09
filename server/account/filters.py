import django_filters as filters

from .models import *


class SubscriptionFilter(filters.FilterSet):

    class Meta:
        model = Subscription
        fields = {"user"}
