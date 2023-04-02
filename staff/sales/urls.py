from django.urls import path

from accounts.decorators import decorate_url_patterns
from staff.sales.views import DashboardView, ProductCreateView, ProductListView, CategoryCreateView, CategoryListView, \
    ProductLoanListView, OrderListView, LoanOrderListView, FAQListView, ProductUpdatedView, CategoryUpdateView, \
    ProfileView, UserChangePasswordView, AssignDriverOrderView, AssignDriverLoanOrderView, FeedbackCreateView, \
    FeedbackListView

app_name = "sales"

urlpatterns = [
    path("feedback/", FeedbackListView.as_view(), name="feedback"),
    path("customer-feedback/<int:customer_id>/", FeedbackCreateView.as_view(), name="customer-feedback"),
    path('assign-driver-loan-order/<pk>/', AssignDriverLoanOrderView.as_view(), name="assign-driver-loan-order"),
    path('assign-driver-order/<pk>/', AssignDriverOrderView.as_view(), name="assign-driver-order"),
    path('change-password/', UserChangePasswordView.as_view(), name="change-password"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('faq-list/', FAQListView.as_view(), name="faq-list"),
    path('loan-order-list/', LoanOrderListView.as_view(), name="loan-order-list"),
    path('order-list/', OrderListView.as_view(), name="order-list"),
    path('product-loan-list/', ProductLoanListView.as_view(), name="product-loan-list"),
    path('category-list/', CategoryListView.as_view(), name="category-list"),
    path('category-update/<int:pk>/', CategoryUpdateView.as_view(), name="category-update"),
    path('category-create/', CategoryCreateView.as_view(), name="category-create"),
    path('product-list/', ProductListView.as_view(), name="product-list"),
    path('product-update/<int:pk>/', ProductUpdatedView.as_view(), name="product-update"),
    path('product-create/', ProductCreateView.as_view(), name="product-create"),
    path('', DashboardView.as_view(), name="index")
]

urlpatterns = decorate_url_patterns(patterns=urlpatterns, user_type="SM")
