from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import *
from .serializers import *


class PublicPromoCodeViewset(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    permission_classes = (AllowAny,)


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
