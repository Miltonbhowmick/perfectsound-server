from rest_framework import viewsets
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import *
from .serializers import *

import stripe
from decouple import config


stripe.api_key = config("PERFECTSOUND_STRIPE_SECRET_KEY")


class PublicPromoCodeViewset(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    permission_classes = (AllowAny,)

    @action(
        methods=["post"],
        detail=False,
        serializer_class=ApplyPromoCodeSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def promo_validate(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            promo_code = serializer.save()
            return Response(
                PromoCodeSerializer(promo_code).data,
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "valid": False,
                "error": "Promo code does not exist or is not currently valid.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )


class PublicPricePlanCreditViewset(viewsets.ModelViewSet):
    queryset = PricePlanCredit.objects.all()
    serializer_class = PricePlanCreditSerializer
    permission_classes = (AllowAny,)


class PublicPricePlanViewset(viewsets.ModelViewSet):
    queryset = PricePlan.objects.all()
    serializer_class = PricePlanSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        qs = self.queryset.order_by("order")
        return qs


class CreateStripeSetupIntent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        stripe_user, created = StripeCustomer.objects.get_or_create(user=user)

        if created:
            # Create customer on stripe
            customer = stripe.Customer.create(email=user.email, name=user.username)
            stripe_user.customer_id = customer.id
            stripe_user.save()

        if stripe_user == None:
            return Response({"client_secret": None}, status=status.HTTP_404_NOT_FOUND)

        intent = stripe.SetupIntent.create(customer=stripe_user.customer_id)

        return Response(
            {"client_secret": intent.client_secret}, status=status.HTTP_201_CREATED
        )


class RetrieveStripePaymentMethods(APIView):
    """
       {
      "data": [
        {
          "allow_redisplay": "unspecified",
          "billing_details": {
            "address": {
              "city": null,
              "country": "BD",
              "line1": null,
              "line2": null,
              "postal_code": null,
              "state": null
            },
            "email": null,
            "name": null,
            "phone": null
          },
          "card": {
            "brand": "visa",
            "checks": {
              "address_line1_check": null,
              "address_postal_code_check": null,
              "cvc_check": "pass"
            },
            "country": "US",
            "display_brand": "visa",
            "exp_month": 1,
            "exp_year": 2039,
            "fingerprint": "9asdnaskdn1",
            "funding": "credit",
            "generated_from": null,
            "last4": "4242",
            "networks": {
              "available": [
                "visa"
              ],
              "preferred": null
            },
            "three_d_secure_usage": {
              "supported": true
            },
            "wallet": null
          },
          "created": 0120232,
          "customer": "cus_Onidas92snd",
          "id": "pm_4o2josDaosdnsdsd",
          "livemode": false,
          "metadata": {},
          "object": "payment_method",
          "type": "card"
        }
      ],
      "has_more": false,
      "object": "list",
      "url": "/v1/payment_methods"
    }
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            stripe_customer = StripeCustomer.objects.get(user=user)
        except StripeCustomer.DoesNotExist:
            return Response(
                {"error": "No Stripe customer found for this user'"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=stripe_customer.customer_id
            )
            return Response(payment_methods["data"], status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
