from django.contrib import admin
from django.contrib.admin import ModelAdmin

from accounts.mixins import ExportCsvMixin
from loan.forms import SavingModelForm, SavingTransactionModelForm
from loan.models import Saving, SavingTransaction, LoanRepayment, LoanRepaymentTransaction, LoanApplication, LoanAccount


@admin.register(Saving)
class SavingAdmin(ExportCsvMixin, ModelAdmin):
    form = SavingModelForm
    add_form = SavingModelForm
    search_fields = ['user__name']
    list_display = ['user', 'amount', 'created', 'updated']
    list_display_links = ['user']
    search_help_text = "Search by user name"
    list_filter = ('updated', 'created')
    # actions = ['export_as_csv']

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    @staticmethod
    def has_change_permission(request, obj=None):
        return True


@admin.register(LoanApplication)
class LoanApplicationAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['user__name']
    list_display = ['user', 'amount', 'purpose', 'status', 'type', 'created', 'updated']
    list_display_links = ['user']
    search_help_text = "Search by user name"
    list_filter = ('status', 'type', 'updated', 'created')
    # actions = ['export_as_csv']

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    @staticmethod
    def has_change_permission(request, obj=None):
        return True

        return True

@admin.register(LoanAccount)
class LoanAccountAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['applicant']
    list_display = ['applicant', 'amount', 'created', 'updated']
    list_display_links = ['applicant']
    search_help_text = "Search by applicant name"
    list_filter = ('updated', 'created')
    # actions = ['export_as_csv']

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    @staticmethod
    def has_change_permission(request, obj=None):
        return True

        return True

    def applicant(self, obj):
        return obj.user.name


@admin.register(SavingTransaction)
class SavingTransactionAdmin(ExportCsvMixin, ModelAdmin):
    form = SavingTransactionModelForm
    add_form = SavingTransactionModelForm
    search_fields = ['mpesa_code']
    list_display = ['saving', 'amount', 'mpesa_code', 'created', 'updated']
    list_display_links = ['saving']
    search_help_text = "Search by user mpesa code"
    list_filter = ('updated', 'created')
    # actions = ['export_as_csv']

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions


    @staticmethod
    def has_change_permission(request, obj=None):
        return True

from loan.models import Account

@admin.register(Account)
class AccountAdmin(ExportCsvMixin, ModelAdmin):
    list_display = ['name', 'amount']

admin.site.register(LoanRepayment)
admin.site.register(LoanRepaymentTransaction)
