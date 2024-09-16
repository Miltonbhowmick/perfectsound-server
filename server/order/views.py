from rest_framework import viewsets
from rest_framework.views import APIView
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


class PublicDownloadViewset(viewsets.ModelViewSet):
    queryset = Download.objects.all()
    serializer_class = DownloadSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context


class UserCreditsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            user_credits = UserCredits.objects.get(user=user)
            return Response(
                {
                    "total_credits": user_credits.total_credits,
                    "used_credits": user_credits.used_credits,
                    "remaining_credits": user_credits.remaining_credits,
                },
                status=status.HTTP_200_OK,
            )
        except UserCredits.DoesNotExist:
            return Response(
                {"error": "User credits not found"}, status=status.HTTP_404_NOT_FOUND
            )
