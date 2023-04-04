from django.contrib import admin
from .models import SupplyTender
from django.contrib import admin

# Register your models here.
class SupplyTenderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity','price',  'tender_status')
    list_filter = ('product', )
    ordering = ()
    search_fields = ('user', 'product')

admin.site.register(SupplyTender, SupplyTenderAdmin)