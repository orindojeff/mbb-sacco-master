
from braces.views import UserFormKwargsMixin
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, UpdateView, CreateView
from accounts.forms import UserModelForm, ProfileModelForm, FeedbackModelForm
from accounts.mixins import ProfileMixin
from accounts.models import FAQ, Profile, Feedback
from stock.mixins import CartMixin, GeneratePdfMixin

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
from accounts.models import User



class DashboardView(CartMixin, TemplateView):
    template_name = 'dispatch/index.html'




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
    template_name = "dispatch/faq.html"

    def get_queryset(self):
        return FAQ.objects.all()


class ProfileView(ProfileMixin, SuccessMessageMixin, UpdateView):
    template_name = "dispatch/profile.html"
    user_form = UserModelForm
    model = Profile
    form_class = ProfileModelForm
    success_message = "Profile has been updated successfully"
    success_url = reverse_lazy("dispatch:index")


class UserChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'dispatch/change-password.html'
    success_url = reverse_lazy('dispatch:index')
    success_message = 'Your password was successfully updated!'
    form_class = PasswordChangeForm


class AssignDriverOrderView(SuccessMessageMixin, CreateView):
    template_name = "dispatch/order-list.html"
    success_url = reverse_lazy("dispatch:order-list")
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
    template_name = "dispatch/feedback-list.html"
    context_object_name = "dialog_list"

    def get_queryset(self):
        return DialogsModel.objects.filter(staff__type="SM")
