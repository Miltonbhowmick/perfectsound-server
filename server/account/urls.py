from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = "account"

router = DefaultRouter()
router.register(r"users", PublicUserViewset, basename="users")


urlpatterns = [path("public/", include(router.urls))]
