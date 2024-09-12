from django.contrib import admin

from .models import *

admin.site.register(PricePlan)
admin.site.register(PricePlanCredit)
admin.site.register(PromoCode)


class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "customer_id", "created_at", "updated_at")


admin.site.register(StripeCustomer, StripeCustomerAdmin)
