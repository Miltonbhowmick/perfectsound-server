from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .models import *
from .serializers import *


class PublicCategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class PublicSubCategoryViewset(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (AllowAny,)


class PublicFavouriteViewset(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = self.queryset.filter(user=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.action == "create":
            return FavouriteTrackCreateSerializer
        return FavouriteSerializer

    def create(self, request, *args, **kwargs):

        user = request.user
        serializer = self.get_serializer(data=request.data, context={"user": user})
        if serializer.is_valid():
            new_favorite_track = serializer.save()
            return Response(
                FavouriteSerializer(new_favorite_track).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
