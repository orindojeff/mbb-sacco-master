from django.urls import path 
from .views import *

app_name = 'dispatch'

urlpatterns = [

	path('', DashboardView.as_view(), name="index"),
	path("feedback/", FeedbackListView.as_view(), name="feedback"),
    path("customer-feedback/<int:customer_id>/", FeedbackCreateView.as_view(), name="customer-feedback"),
    path('assign-driver-loan-order/<pk>/', AssignDriverLoanOrderView.as_view(), name="assign-driver-loan-order"),
    path('assign-driver-order/<pk>/', AssignDriverOrderView.as_view(), name="assign-driver-order"),
    path('change-password/', UserChangePasswordView.as_view(), name="change-password"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('faq-list/', FAQListView.as_view(), name="faq-list"),
    path('loan-order-list/', LoanOrderListView.as_view(), name="loan-order-list"),
    path('order-list/', OrderListView.as_view(), name="order-list"),


]