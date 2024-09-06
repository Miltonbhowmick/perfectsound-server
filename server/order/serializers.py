from rest_framework import serializers

from .models import *
from account.models import User
from payment.models import PricePlan, PromoCode


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=True
    )
    price_plan = serializers.PrimaryKeyRelatedField(queryset=PricePlan.objects.all())
    promo_code = serializers.PrimaryKeyRelatedField(
        queryset=PromoCode.objects.all(),
        required=False,
    )
    company = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=True
    )
    address1 = serializers.CharField(max_length=255)
    address2 = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=True
    )
    country = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    state = serializers.CharField(max_length=255)
    zip_code = serializers.CharField(max_length=255)
    is_agreed_policy = serializers.BooleanField()

    def create(self, validated_data):
        user = self.context["user"]
        new_order = Order.objects.create(**validated_data)
        if user:
            new_order.user = user
            new_order.save()
        return new_order
