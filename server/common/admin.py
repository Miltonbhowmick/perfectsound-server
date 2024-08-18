from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(SubCategory)


class FavouriteAdmin(admin.ModelAdmin):
    list_display = ["user"]

    search_fields = ["user"]


admin.site.register(Favorite, FavouriteAdmin)
