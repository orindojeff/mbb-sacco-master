from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from accounts.forms import ProfileModelForm, UserModelForm, StaffFeedbackModelForm
from accounts.mixins import ProfileMixin
from accounts.models import FAQ, Profile, Feedback, DialogsModel
from client.helpers import create_dialog_
from delivery.forms import OrderDeliveryModelForm, LoanOrderDeliveryModelForm
from delivery.models import OrderDelivery, UserPickUpStation
from stock.forms import ProductModelForm, CategoryModelForm
from stock.models import Product, Category, ProductLoan, Order, LoanOrder

User: AbstractUser = get_user_model()


class DashboardView(TemplateView):
    template_name = "sales/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_loan_order'] = LoanOrder.objects.filter(complete=False)
        context['pending_order'] = Order.objects.filter(complete=False)
        return context


class ProductCreateView(SuccessMessageMixin, CreateView):
    template_name = "sales/product-create.html"
    form_class = ProductModelForm
    success_message = "product has been added successfully"
    success_url = reverse_lazy("sales:product-list")


class ProductUpdatedView(SuccessMessageMixin, UpdateView):
    model = Product
    template_name = "sales/product-create.html"
    form_class = ProductModelForm
    success_message = "product has been updated successfully"
    success_url = reverse_lazy("sales:product-list")


class ProductListView(ListView):
    template_name = "sales/product-list.html"

    def get_queryset(self):
        return Product.objects.all()


class CategoryCreateView(SuccessMessageMixin, CreateView):
    template_name = "sales/category-create.html"
    form_class = CategoryModelForm
    success_message = "category has been added successfully."
    success_url = reverse_lazy("sales:category-list")


class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    template_name = "sales/category-create.html"
    form_class = CategoryModelForm
    success_message = "category has been updated successfully."
    success_url = reverse_lazy("sales:category-list")


class CategoryListView(ListView):
    template_name = "sales/category-list.html"

    def get_queryset(self):
        return Category.objects.all()


class ProductLoanListView(ListView):
    template_name = "sales/product-loan-list.html"

    def get_queryset(self):
        return ProductLoan.objects.all()


class OrderListView(ListView):
    template_name = "sales/order-list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['drivers'] = User.objects.filter(type="DR", is_active=True)
        return context

    def get_queryset(self):
        return Order.objects.all()


class LoanOrderListView(ListView):
    template_name = "sales/loan-order-list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['drivers'] = User.objects.filter(type="DR", is_active=True)
        return context

    def get_queryset(self):
        return LoanOrder.objects.all()


class FAQListView(ListView):
    template_name = "sales/faq.html"

    def get_queryset(self):
        return FAQ.objects.all()


class ProfileView(ProfileMixin, SuccessMessageMixin, UpdateView):
    template_name = "sales/profile.html"
    user_form = UserModelForm
    model = Profile
    form_class = ProfileModelForm
    success_message = "Profile has been updated successfully"
    success_url = reverse_lazy("sales:index")


class UserChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'sales/change-password.html'
    success_url = reverse_lazy('sales:index')
    success_message = 'Your password was successfully updated!'
    form_class = PasswordChangeForm


class AssignDriverOrderView(SuccessMessageMixin, CreateView):
    template_name = "sales/order-list.html"
    success_url = reverse_lazy("sales:order-list")
    success_message = "Order has been assigned successfully."
    form_class = OrderDeliveryModelForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        order = get_object_or_404(Order, pk=self.kwargs.get("pk", None))
        instance.order = order
        order.assigned = True
        order.save()
        instance.station = get_object_or_404(UserPickUpStation, user=order.user, selected=True)
        return super().form_valid(form)


class AssignDriverLoanOrderView(SuccessMessageMixin, CreateView):
    template_name = "sales/loan-order-list.html"
    success_url = reverse_lazy("sales:order-list")
    success_message = "Loan order has been assigned successfully."
    form_class = LoanOrderDeliveryModelForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        order = get_object_or_404(LoanOrder, pk=self.kwargs.get("pk", None))
        instance.order = order
        order.assigned = True
        order.save()
        instance.station = get_object_or_404(UserPickUpStation, user=order.user, selected=True)
        return super().form_valid(form)


class FeedbackCreateView(SuccessMessageMixin, CreateView):
    template_name = "sales/feedback.html"
    form_class = StaffFeedbackModelForm
    model = Feedback
    success_message = "feedback has been sent successfully"

    def get_success_url(self):
        return reverse_lazy("sales:customer-feedback", kwargs=dict(customer_id=self.kwargs.get("customer_id")))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedback_list'] = Feedback.objects.filter(
            Q(type="CST_SMR") | Q(type="SMR_CST"),
            dialog__customer_id=self.kwargs.get("customer_id"),
        ).order_by("created")
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.dialog_id = create_dialog_(
            user_id=self.kwargs.get("customer_id"), feedback_type=instance.type, staff_id=self.request.user.pk
        )
        instance.type = "SMR_CST"
        return super().form_valid(form)


class FeedbackListView(ListView):
    template_name = "sales/feedback-list.html"
    context_object_name = "dialog_list"

    def get_queryset(self):
        return DialogsModel.objects.filter(staff__type="SM")
