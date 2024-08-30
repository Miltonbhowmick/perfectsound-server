from rest_framework import serializers

from .models import *


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = "__all__"


class PricePlanCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePlanCredit
        fields = "__all__"


class PricePlanSerializer(serializers.ModelSerializer):
    credits = PricePlanCreditSerializer(many=True, source="credit")

    class Meta:
        model = PricePlan
        fields = [
            "id",
            "order",
            "title",
            "duration",
            "duration_unit",
            "description",
            "amount",
            "credits",
        ]
