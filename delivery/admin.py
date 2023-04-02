from django.contrib import admin
from django.contrib.admin import ModelAdmin

from accounts.mixins import ExportCsvMixin
from delivery.forms import LocationModelForm, PickUpStationModelForm, AdminUserPickUpStationModelForm
from delivery.models import Location, PickUpStation, UserPickUpStation, OrderDelivery, LoanOrderDelivery


@admin.register(Location)
class LocationAdmin(ExportCsvMixin, ModelAdmin):
    form = LocationModelForm
    add_form = LocationModelForm
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


@admin.register(PickUpStation)
class PickUpStationAdmin(ExportCsvMixin, ModelAdmin):
    form = PickUpStationModelForm
    add_form = PickUpStationModelForm
    search_fields = ['name']
    list_display = ['name', 'location', 'created', 'updated']
    list_display_links = ['name', 'location']
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


@admin.register(UserPickUpStation)
class UserPickUpStationAdmin(ExportCsvMixin, ModelAdmin):
    form = AdminUserPickUpStationModelForm
    add_form = AdminUserPickUpStationModelForm
    list_display = ['user', 'station', 'created', 'updated']
    list_display_links = ['user', 'station']
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


admin.site.register(OrderDelivery)
admin.site.register(LoanOrderDelivery)
