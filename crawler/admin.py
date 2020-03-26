from django.contrib import admin
from .models import StoreItem_dj, BaseItem_dj, ScrapyItem

class StoreItem_djAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_id', 'store_name', 'store_id', 'price']

class BaseItem_djAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_id', 'hole_num', 'equipment_location']
class BaseItem_djAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_id', 'hole_num', 'equipment_location']

class ScrapyItemAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'item_num']

admin.site.register(StoreItem_dj, StoreItem_djAdmin)
admin.site.register(BaseItem_dj, BaseItem_djAdmin)
admin.site.register(ScrapyItem, ScrapyItemAdmin)