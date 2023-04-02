from django.urls import path

from client.rider.views import DashboardView, AppliedLoanListView, FAQListView, ProfileView, UserChangePasswordView, \
    LoanApplyView, LoanRepaymentView, LoanRepaymentListView, OrderListView, OrderPaymentListView, ProductListView, \
    OrderPdfView, SavingView, AddToCartView, RemoveFromCartView, DeleteItemFromCartView, CartListView, CheckoutView, \
    OrderPaymentPdfView, ProductLoanView, ProductLoanOrderListView, ProductLoanCheckoutView, \
    ProductLoanPaymentListView, SearchView, ProductDetailView, PayProductLoanView, PickUpStationView, pick_order, \
    pick_loan_order, PickUpStationUpdateView, SelectedPickUpStationListView, OrderDeliveryListView, \
    LoanOrderDeliveryListView, select_pickup_station, OrderDeliveryDetailView, SavingsWithdrawalCreateView, \
    FeedbackCreateView, confirm_order_picked

app_name = "rider"

urlpatterns = [
    path("feedback/", FeedbackCreateView.as_view(), name="feedback"),
    path('confirm-picked/<int:pk>/', confirm_order_picked, name="confirm-picked"),
    path('select-pickup-station/<int:pk>/', select_pickup_station, name="select-pickup-station"),
    path('pick-loan-order/<int:pk>/', pick_loan_order, name="pick-loan-order"),
    path('pick-order/<int:pk>/', pick_order, name="pick-order"),
    path('order-delivery-detail/<int:pk>/', OrderDeliveryDetailView.as_view(), name="order-delivery-detail"),
    path('product-detail/<int:pk>/', ProductDetailView.as_view(), name="product-detail"),
    path('delete-from-cart/<int:product_id>/', DeleteItemFromCartView.as_view(), name="delete-from-cart"),
    path('remove-from-cart/<int:product_id>/', RemoveFromCartView.as_view(), name="remove-from-cart"),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name="add-to-cart"),
    path('order-product-loan/<int:product_id>/', ProductLoanView.as_view(), name="order-product-loan"),
    path('order-payment-pdf/<int:pk>/', OrderPaymentPdfView.as_view(), name="order-payment-pdf"),
    path('order-pdf/<int:pk>/', OrderPdfView.as_view(), name="order-pdf"),
    path('product-loan-checkout/<int:pk>/', ProductLoanCheckoutView.as_view(), name="product-loan-checkout"),
    path('product-loan-payment-list/', ProductLoanPaymentListView.as_view(), name="product-loan-payment-list"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('loan-order-list/', ProductLoanOrderListView.as_view(), name="loan-order-list"),
    path('savings-withdrawal/', SavingsWithdrawalCreateView.as_view(), name="savings-withdrawal"),
    path('cart-list/', CartListView.as_view(), name="cart-list"),
    path('change-password/', UserChangePasswordView.as_view(), name="change-password"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('faq-list/', FAQListView.as_view(), name="faq-list"),
    path('product-list/', ProductListView.as_view(), name="product-list"),
    path('order-payment-list/', OrderPaymentListView.as_view(), name="order-payment-list"),
    path('order-list/', OrderListView.as_view(), name="order-list"),
    path('loan-repayment-list/', LoanRepaymentListView.as_view(), name="loan-repayment-list"),
    path('loan-repayment/', LoanRepaymentView.as_view(), name="loan-repayment"),
    path('apply-loan/', LoanApplyView.as_view(), name="apply-loan"),
    path('saving/', SavingView.as_view(), name="saving"),
    path('search/', SearchView.as_view(), name="search"),
    path('applied-loan-list/', AppliedLoanListView.as_view(), name="applied-loan-list"),
    path('pay-product-loan/', PayProductLoanView.as_view(), name="pay-product-loan"),
    path('selected-pickup-station/', SelectedPickUpStationListView.as_view(), name="selected-pickup-station"),
    path('update-pickup-station/<int:pk>/', PickUpStationUpdateView.as_view(), name="update-pickup-station"),
    path('pickup-station/', PickUpStationView.as_view(), name="pickup-station"),
    path('order-delivery-list/', OrderDeliveryListView.as_view(), name="order-delivery-list"),
    path('loan-order-delivery-list/', LoanOrderDeliveryListView.as_view(), name="loan-order-delivery-list"),
    path('', DashboardView.as_view(), name="index"),
]
