from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import *

app_name = "order"

router = DefaultRouter()
router.register(r"orders", PublicOrderViewset, basename="orders")

urlpatterns = [path("public/", include(router.urls))]
