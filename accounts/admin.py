from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ngettext

from .forms import UserAdminChangeForm, AdminRegistrationForm
from .mixins import ExportCsvMixin
from .models import User, Profile, FAQ

admin.site.site_header = "MIGORI BODA BODA SACCO ADMIN "
admin.site.site_title = "Migori Boda Boda SACCO "
admin.site.index_title = "MIGORI BODA BODA SACCO"

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(ExportCsvMixin, BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = AdminRegistrationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'email', 'username', 'type')
    search_fields = ('name', 'email', 'username',)
    list_filter = ('is_active', 'is_verified', 'is_archived', 'updated', 'created', 'type')
    actions = ['make_active', 'make_inactive', 'export_as_csv']

    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal info', {'fields': ('name', 'email', 'username')}),
        ('Permissions', {'fields': ('type',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'username', 'type', 'password1', 'password2')}
         ),
    )
    ordering = ['email']
    filter_horizontal = ()

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True, is_verified=True, is_archived=False)
        self.message_user(request, ngettext(
            '%d User has successfully been marked as active.',
            '%d Users have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Activate User"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False, is_archived=True)
        self.message_user(request, ngettext(
            '%d User has been archived successfully.',
            '%d Users have been archived successfully.',
            updated,
        ) % updated, messages.INFO)

    make_inactive.short_description = "Archive User"

    @staticmethod
    def has_delete_permission(request, obj=None):
        return False

    @staticmethod
    def has_change_permission(request, obj=None):
        return True

    @staticmethod
    def has_add_permission(request, obj=None):
        return True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Profile)
class ProfileAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['user__name']
    list_display = ['user', 'phone_number', 'image', 'gender']
    list_display_links = ['user', 'gender']
    search_help_text = "Search by name"
    list_filter = ('gender', 'updated', 'created')
    actions = ['export_as_csv']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    @staticmethod
    def has_change_permission(request, obj=None):
        return True


@admin.register(FAQ)
class FAQAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'type', 'created', 'updated']
    list_display_links = ['name']
    search_help_text = "Search by name"
    list_filter = ('type', 'updated', 'created')
    actions = ['export_as_csv']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    @staticmethod
    def has_change_permission(request, obj=None):
        return True
