from django.urls import path

from accounts.decorators import decorate_url_patterns
from client.customer.views import DashboardView, ProductDetailView, AddToCartView, RemoveFromCartView, \
    DeleteItemFromCartView, CartListView, OrderPdfView, OrderListView, OrderPaymentListView, ProductListView, \
    FAQListView, ProfileView, UserChangePasswordView, SearchView, CheckoutView, OrderPaymentPdfView, PickUpStationView, \
    pick_loan_order, pick_order, SelectedPickUpStationListView, PickUpStationUpdateView, OrderDeliveryListView, \
    select_pickup_station, OrderDeliveryDetailView, FeedbackCreateView, confirm_order_picked

app_name = "customer"

urlpatterns = [
    path("feedback/", FeedbackCreateView.as_view(), name="feedback"),
    path('confirm-picked/<int:pk>/', confirm_order_picked, name="confirm-picked"),
    path('order-delivery-detail/<int:pk>/', OrderDeliveryDetailView.as_view(), name="order-delivery-detail"),
    path('order-delivery-list/', OrderDeliveryListView.as_view(), name="order-delivery-list"),
    path('select-pickup-station/<int:pk>/', select_pickup_station, name="select-pickup-station"),
    path('pick-loan-order/<int:pk>/', pick_loan_order, name="pick-loan-order"),
    path('pick-order/<int:pk>/', pick_order, name="pick-order"),
    path('cart-list/', CartListView.as_view(), name="cart-list"),
    path('product-detail/<int:pk>/', ProductDetailView.as_view(), name="product-detail"),
    path('delete-from-cart/<int:product_id>/', DeleteItemFromCartView.as_view(), name="delete-from-cart"),
    path('remove-from-cart/<int:product_id>/', RemoveFromCartView.as_view(), name="remove-from-cart"),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name="add-to-cart"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('search/', SearchView.as_view(), name="search"),
    path('change-password/', UserChangePasswordView.as_view(), name="change-password"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('faq-list/', FAQListView.as_view(), name="faq-list"),
    path('order-payment-pdf/<int:pk>/', OrderPaymentPdfView.as_view(), name="order-payment-pdf"),
    path('order-pdf/<int:pk>/', OrderPdfView.as_view(), name="order-pdf"),
    path('product-list/', ProductListView.as_view(), name="product-list"),
    path('order-payment-list/', OrderPaymentListView.as_view(), name="order-payment-list"),
    path('order-list/', OrderListView.as_view(), name="order-list"),
    path('selected-pickup-station/', SelectedPickUpStationListView.as_view(), name="selected-pickup-station"),
    path('update-pickup-station/<int:pk>/', PickUpStationUpdateView.as_view(), name="update-pickup-station"),
    path('pickup-station/', PickUpStationView.as_view(), name="pickup-station"),
    path('', DashboardView.as_view(), name="index"),
]

urlpatterns = decorate_url_patterns(patterns=urlpatterns, user_type="CM")
