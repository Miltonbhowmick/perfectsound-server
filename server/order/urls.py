from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import *

app_name = "order"

router = DefaultRouter()
router.register(r"orders", PublicOrderViewset, basename="orders")
router.register(r"downloads", PublicDownloadViewset, basename="downloads")

urlpatterns = [
    path("public/", include(router.urls)),
    path("user/credits/", UserCreditsView.as_view(), name="user_credits"),
]
