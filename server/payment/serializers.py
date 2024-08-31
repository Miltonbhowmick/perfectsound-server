from rest_framework import serializers

from .models import *
from django.utils import timezone


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = "__all__"


class ApplyPromoCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, value):
        if value:
            try:
                promo_code = PromoCode.objects.get(title=value)
            except:
                raise serializers.ValidationError("Invalid Promo Code!")

            now = timezone.now()
            if (
                promo_code.is_active == False
                or promo_code.start_date is None
                or promo_code.start_date > now
                or promo_code.end_date is None
                or promo_code.end_date < now
            ):
                raise serializers.ValidationError(
                    "Promo Code is currently not available"
                )


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
