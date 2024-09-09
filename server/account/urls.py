from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = "account"

router = DefaultRouter()
router.register(r"users", PublicUserViewset, basename="users")
router.register(r"subscriptions", PublicSubscriptionViewset, basename="subscriptions")


urlpatterns = [path("public/", include(router.urls))]
