from django.contrib import admin

from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "price_plan", "created_at", "updated_at")


admin.site.register(Order, OrderAdmin)
admin.site.register(UserCredits)
admin.site.register(Transaction)
admin.site.register(Download)
