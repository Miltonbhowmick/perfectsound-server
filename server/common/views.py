from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import *
from .serializers import *


class PublicCategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class PublicFavouriteViewset(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = self.queryset.filter(user=self.request.user)
        return qs
