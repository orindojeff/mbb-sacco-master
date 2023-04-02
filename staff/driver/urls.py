from django.urls import path

from staff.driver.views import DashboardView, UserChangePasswordView, ProfileView, FAQListView, confirm_delivered_order, \
    confirm_delivered_loan_order, AssignedOrdersListView, \
    AssignedLoanOrdersListView, mark_order_delivery_status_as_in_transit, mark_order_delivery_status_as_arrived, \
    mark_loan_order_delivery_status_as_in_transit, mark_loan_order_delivery_status_as_arrived, OrderDeliveryListView, \
    InTransitOrderDeliveryListView, CompletedOrderDeliveryListView, LoanOrderDeliveryListView, \
    InTransitLoanOrderDeliveryListView, CompletedLoanOrderDeliveryListView

app_name = "driver"

urlpatterns = [
    path('mark-loan-order-as-arrived/<int:pk>/', mark_loan_order_delivery_status_as_arrived,
         name="mark-loan-order-as-arrived"),
    path('mark-loan-order-as-in-transit/<int:pk>/', mark_loan_order_delivery_status_as_in_transit,
         name="mark-loan-order-as-in-transit"),
    path('mark-order-as-arrived/<int:pk>/', mark_order_delivery_status_as_arrived,
         name="mark-order-as-arrived"),
    path('mark-order-as-in-transit/<int:pk>/', mark_order_delivery_status_as_in_transit,
         name="mark-order-as-in-transit"),
    path('confirm-loan-order/<int:pk>/', confirm_delivered_loan_order, name="confirm-loan-order"),
    path('confirm-order/<int:pk>/', confirm_delivered_order, name="confirm-order"),
    path('loan-order-delivery/', LoanOrderDeliveryListView.as_view(), name="loan-order-delivery"),
    path('completed-loan-order-delivery/', CompletedLoanOrderDeliveryListView.as_view(),
         name="completed-loan-order-delivery"),
    path('in-transit-loan-order-delivery/', InTransitLoanOrderDeliveryListView.as_view(),
         name="in-transit-loan-order-delivery"),
    path('order-delivery/', OrderDeliveryListView.as_view(), name="order-delivery"),
    path('completed-order-delivery/', CompletedOrderDeliveryListView.as_view(), name="completed-order-delivery"),
    path('in-transit-order-delivery/', InTransitOrderDeliveryListView.as_view(), name="in-transit-order-delivery"),
    # path('assigned-loan-order-list/', AssignedLoanOrdersListView.as_view(), name="assigned-loan-order-list"),
    # path('assigned-order-list/', AssignedOrdersListView.as_view(), name="assigned-order-list"),
    path('change-password/', UserChangePasswordView.as_view(), name="change-password"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('faq-list/', FAQListView.as_view(), name="faq-list"),
    path('', DashboardView.as_view(), name="index"),
]
