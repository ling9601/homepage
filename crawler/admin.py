from django.contrib import admin
from .models import StoreItem_dj

class StoreItem_djAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_id', 'store_name', 'store_id', 'price']

admin.site.register(StoreItem_dj, StoreItem_djAdmin)