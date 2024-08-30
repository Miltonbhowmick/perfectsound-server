from rest_framework import serializers

from .models import *
from account.models import User
from payment.models import PricePlan, PromoCode


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    phone_number = serializers.CharField(max_length=100, required=True)
    price_plan = serializers.PrimaryKeyRelatedField(
        queryset=PricePlan.objects.all(), required=True
    )
    promo_code = serializers.PrimaryKeyRelatedField(
        queryset=PromoCode.objects.all(), required=False, allow_null=True
    )
    company = serializers.CharField(max_length=255, required=False, allow_null=True)
    address1 = serializers.CharField(max_length=255, required=True)
    address2 = serializers.CharField(max_length=255, required=False, allow_null=True)
    country = serializers.CharField(max_length=255, required=True)
    city = serializers.CharField(max_length=255, required=True)
    street = serializers.CharField(max_length=255, required=True)
    is_agreed_policy = serializers.BooleanField(required=True)

    def create(self, validated_data):
        user = self.context["user"]
        new_order = Order.objects.create(**validated_data)
        if user:
            new_order.user = user
            new_order.save()
        return new_order
