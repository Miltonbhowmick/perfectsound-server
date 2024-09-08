from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import *

app_name = "payment"

router = DefaultRouter()
router.register(r"price-plans", PublicPricePlanViewset, basename="priceplans")
router.register(r"promo-codes", PublicPromoCodeViewset, basename="promocodes")
router.register(
    r"price-plan-credits", PublicPricePlanCreditViewset, basename="priceplancredits"
)

urlpatterns = [
    path("public/", include(router.urls)),
]
