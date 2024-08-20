from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

app_name = "common"

router = DefaultRouter()
router.register(r"categories", PublicCategoryViewset, basename="categories")
router.register(r"subcategories", PublicSubCategoryViewset, basename="subcategories")
router.register(r"favourites", PublicFavouriteViewset, basename="favourites")

urlpatterns = [path("public/", include(router.urls))]
