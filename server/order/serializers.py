from rest_framework import serializers

from .models import *
from account.models import User
from payment.models import (
    PricePlan,
    PromoCode,
    PricePlanCredit,
)
from music.models import Track
from payment.serializers import PricePlanSerializer, PricePlanCreditSerializer
from payment.utils.choices import DurationChoices
from account.models import Subscription


class OrderSerializer(serializers.ModelSerializer):
    price_plan = PricePlanSerializer()
    price_plan_credit = PricePlanCreditSerializer()

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
    credit = serializers.PrimaryKeyRelatedField(
        queryset=PricePlanCredit.objects.all(),
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
        credit = validated_data.pop("credit", None)
        new_order = Order.objects.create(**validated_data)
        new_order.price_plan_credit = credit

        if user:
            new_order.user = user
        new_order.save()

        # Create subscription based on the order
        # But the subscription will not active until payment complete
        new_subscription = Subscription.objects.create(user=user, order=new_order)

        return new_order


class DownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Download
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["user"]
        track_id = validated_data.get("track_id", None)
        if track_id:
            try:
                track = Track.objects.get(track_id)
                # Download music
                download_music, created = Download.objects.get_or_create(
                    user=user, track=track
                )
                if created:
                    # New transaction on download music
                    new_transaction = Transaction.objects.create(user=user, track=track)
                    # Re-calculate user credits amount
                    user_credits = UserCredits.objects.get(user=user)
                    user_credits.used_credits += track.credits
                    user_credits.remaining_credits -= track.credits
                    user_credits.save()
                else:
                    raise serializers.ValidationError(
                        {"valid": False, "error": "You have already download music"}
                    )

            except Track.DoesNotExist:
                raise serializers.ValidationError(
                    {"valid": False, "error": "Music track is not exists!"}
                )

        else:
            raise serializers.ValidationError(
                {"valid": False, "error": "Track must be provided!"}
            )
