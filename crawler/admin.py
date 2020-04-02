from django.contrib import admin
from .models import *

class StoreItem_djAdmin(admin.ModelAdmin):
    list_display = ['base_item', 'store_name', 'store_id', 'price']

class BaseItem_djAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_id', 'hole_num', 'equipment_location']

class ScrapyItemAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'time_cost', 'item_num', 'fail_num']

class WantedItemAdmin(admin.ModelAdmin):
    list_display = ['base_item', 'level', 'upper_price', 'time']

# class CatchedItemAdmin(admin.ModelAdmin):
#     list_display = ['wanted_item', 'store_item', 'time']

admin.site.register(StoreItem_dj, StoreItem_djAdmin)
admin.site.register(BaseItem_dj, BaseItem_djAdmin)
admin.site.register(WantedItem, WantedItemAdmin)
# admin.site.register(CatchedItem, CatchedItemAdmin)
admin.site.register(ScrapyItem, ScrapyItemAdmin)