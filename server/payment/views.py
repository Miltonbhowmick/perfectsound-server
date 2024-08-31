from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


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
            return Response(
                {
                    "valid": True,
                    "error": "Promo code is currently valid.",
                },
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
