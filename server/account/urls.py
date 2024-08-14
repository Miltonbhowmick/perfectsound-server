from django.urls import path, include
from .views import *
from rest_framework import routers

app_name = "account"

router = routers.DefaultRouter()
router.register(
    r"users",
    PublicUserViewset,
)


urlpatterns = [path("public/", include(router.urls))]
