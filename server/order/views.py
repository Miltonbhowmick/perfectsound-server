from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


class PublicOrderViewset(viewsets.ModelViewSet):
    """
    {
        "id": 8,
        "first_name": "",
        "last_name": "",
        "phone_number": "",
        "company": "",
        "address1": "",
        "address2": "",
        "country": "",
        "city": "",
        "state": "",
        "zip_code": "",
        "is_agreed_policy": false,
        "price_plan": 3,
        "promo_code": promo_code,
    }
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == "list":
            return qs.filter(user=self.request.user)
        return qs

    def create(self, request):
        serializer = OrderCreateSerializer(
            data=request.data, context={"user": self.request.user}
        )
        if serializer.is_valid():
            new_order = serializer.save()
            return Response(
                self.serializer_class(new_order).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
