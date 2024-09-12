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

        if (
            StripeCustomer.objects.filter(user=user)
            .filter(Q(customer_id__isnull=False))
            .exists()
            == False
        ):
            # Create customer on stripe
            customer = stripe.Customer.create(email=user.email, name=user.username)
            print(customer)
            stripe_user = StripeCustomer.objects.create(
                user=user, customer_id=customer.id
            )

        intent = stripe.SetupIntent.create(customer=stripe_user.customer_id)

        return Response({"client_secret": intent.client_secret})
