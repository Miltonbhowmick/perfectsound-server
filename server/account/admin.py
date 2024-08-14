from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "gender",
        "country",
        "is_active",
        "is_staff",
        "join_date",
    )
    list_filter = ("gender", "country", "is_active", "is_staff", "is_superuser")
    search_fields = ("nickname", "email")


admin.site.register(User, UserAdmin)
