from django.contrib import admin
from dashboard.models import *


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'number')


class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'number','warehouse')


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('apikey', 'apisec')


admin.site.register(Warehouse,  WarehouseAdmin)
admin.site.register(Store,  StoreAdmin)
admin.site.register(ApiKey,  ApiKeyAdmin)

