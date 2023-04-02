from django.urls import path

from staff.finance.views import DashboardView, LoanRepaymentList, OrderPaymentList, LoanOrderPaymentList, \
    confirm_loan_repayment, confirm_order_payment, confirm_loan_order_payment, FAQListView, ProfileView, \
    UserChangePasswordView, ApprovedLoanRepaymentList, ApprovedOrderPaymentList, ApprovedLoanOrderPaymentList, \
    FeedbackCreateView, FeedbackListView, LoanApplicationListView, confirm_loan

app_name = "finance"

urlpatterns = [
    path("loan-list/", LoanApplicationListView.as_view(), name="loan-list"),
    path("feedback/", FeedbackListView.as_view(), name="feedback"),
    path("customer-feedback/<int:customer_id>/", FeedbackCreateView.as_view(), name="customer-feedback"),
    path('change-password/', UserChangePasswordView.as_view(), name="change-password"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('faq-list/', FAQListView.as_view(), name="faq-list"),
    path('confirm-loan/<int:pk>/', confirm_loan, name="confirm-loan"),
    path('confirm-loan-order-payment/<int:pk>/', confirm_loan_order_payment, name="confirm-loan-order-payment"),
    path('confirm-order-payment/<int:pk>/', confirm_order_payment, name="confirm-order-payment"),
    path('confirm-loan-repayment/<int:pk>/', confirm_loan_repayment, name="confirm-loan-repayment"),
    path('loan-order-payment-list/', LoanOrderPaymentList.as_view(), name="loan-order-payment-list"),
    path('approved-loan-order-payment-list/', ApprovedLoanOrderPaymentList.as_view(),
         name="approved-loan-order-payment-list"),
    path('order-payment-list/', OrderPaymentList.as_view(), name="order-payment-list"),
    path('approved-order-payment-list/', ApprovedOrderPaymentList.as_view(),
         name="approved-order-payment-list"),
    path('loan-repayment-list/', LoanRepaymentList.as_view(), name="loan-repayment-list"),
    path('approved-loan-repayment-list/', ApprovedLoanRepaymentList.as_view(),
         name="approved-loan-repayment-list"),
    path('', DashboardView.as_view(), name="index"),
]
