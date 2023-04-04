from django.urls import path
from .views import *

app_name='supplier'

urlpatterns = [
        path('supplier', supplier, name='index'),
        path('tender-request/', SupplyTenderCreateView.as_view(), name='tender-request'),
   	    # path('supply_list/', SupplyListView.as_view(), name='supply_list'),
        path('supplied-tenders/', ConfirmTenderListView.as_view(), name='confirm-tenders'),
        path('Complete-tenders/', CompleteTenderListView.as_view(), name='complete-supply-tenders'),
        path('rejected-tenders/', RejectedSupplierTenderListView.as_view(), name='rejected-supply-tenders'),
        path('confirmed-supplied-tenders/', confirmedSupplierTenderListView.as_view(), name='confirmed-supplier-tenders'),
        path('confirm-tenders/', SuppliedTenderListView.as_view(), name='suplied-tenders'),
        path('pending-tenders/', PendingSupplyTenderListView.as_view(), name='pending-tenders'),
        path('supplier-pending-tenders/', PendingTenderListView.as_view(), name='supplier_pending_tenders'),
        path('pay-tenders/', FinanceSupplierTenderListView.as_view(), name='pay-tenders'),
        path('paid-tenders/', PaidTenderListView.as_view(), name='paid-tenders'),
        path('confirmed-paid-tenders/', ConfirmedPaidTenderListView.as_view(), name='confirmed-paid-tenders'),
        path('confirmed-inventory-tenders/', InventoryConfirmTenderListView.as_view(), name='confirmed-inventory-tenders'),
        path('pending-approval-tenders/', PendingApprovalTenderListView.as_view(), name='pending_approval_tenders'),
        path('approved-supplier-tenders/', ApprovedSupplierTenderListView.as_view(), name='approved-supplier-tenders'),
        path('supplier-confirm-tender-payments/', SupplierConfirmRecievedPayments.as_view(), name='supplier-confirm-tender-payments'),
        
]
