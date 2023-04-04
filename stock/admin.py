from django.contrib import admin
from django.contrib.admin import ModelAdmin

from accounts.mixins import ExportCsvMixin
from stock.forms import CategoryModelForm, ProductModelForm, ProductLoanModelForm
from stock.models import Category, Product, ProductLoan, LoanOrder, Order


@admin.register(Category)
class CategoryAdmin(ExportCsvMixin, ModelAdmin):
    form = CategoryModelForm
    add_form = CategoryModelForm
    search_fields = ['name']
    list_display = ['name', 'created', 'updated']
    list_display_links = ['name']
    search_help_text = "Search by name"
    list_filter = ('updated', 'created')
    actions = ['export_as_csv']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    @staticmethod
    def has_change_permission(request, obj=None):
        return True


@admin.register(Product)
class ProductAdmin(ExportCsvMixin, ModelAdmin):
    form = ProductModelForm
    add_form = ProductModelForm
    search_fields = ['name']
    list_display = ['name', 'category', 'amount', 'description', 'quantity', 'image', 'created', 'updated']
    list_display_links = ['name']
    search_help_text = "Search by name"
    list_filter = ('updated', 'created')
    actions = ['export_as_csv']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    @staticmethod
    def has_change_permission(request, obj=None):
        return True
        return True


@admin.register(ProductLoan)
class ProductLoanAdmin(ExportCsvMixin, ModelAdmin):
    form = ProductLoanModelForm
    add_form = ProductLoanModelForm
    search_fields = ['product__name']
    list_display = ['product', 'duration', 'created', 'updated']
    list_display_links = ['product']
    search_help_text = "Search by product name"
    list_filter = ('updated', 'created')
    actions = ['export_as_csv']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    @staticmethod
    def has_change_permission(request, obj=None):
        return True



@admin.register(LoanOrder)
class ProductLoanAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['user']
    list_display = ['transaction_id', 'product_loan']


@admin.register(Order)
class OrderAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['user']
    list_display = ['user', 'transaction_id', 'complete']
   
from stock.models import LoanOrderInstallments


@admin.register(LoanOrderInstallments)
class LoanOrderInstallmentsAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['user']
    list_display = ['transaction_id', 'type', 'confirm']
   
    def transaction_id(self, obj):
        return obj.order.transaction_id