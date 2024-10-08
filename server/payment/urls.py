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
    path(
        "stripe/setup-intent/",
        CreateStripeSetupIntentView.as_view(),
        name="stripe_setup_intent",
    ),
    path(
        "stripe/payment-methods/",
        RetrieveStripePaymentMethods.as_view(),
        name="stripe_payment_methods",
    ),
    path(
        "stripe/payment-confirm/",
        ConfirmPaymentView.as_view(),
        name="stripe_payment_confirm",
    ),
    path(
        "stripe/payment-intent/",
        CreateStripePaymentIntentView.as_view(),
        name="stripe_payment_intent",
    ),
]
