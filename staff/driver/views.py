from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView

from accounts.forms import UserModelForm, ProfileModelForm
from accounts.mixins import ProfileMixin
from accounts.models import Profile, FAQ
from delivery.models import OrderDelivery, LoanOrderDelivery


class DashboardView(TemplateView):
    template_name = "driver/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_order_delivery'] = OrderDelivery.objects.exclude(status="AR")
        context['pending_loan_order_delivery'] = LoanOrderDelivery.objects.exclude(status="AR")
        return context


class FAQListView(ListView):
    template_name = "driver/faq.html"

    def get_queryset(self):
        return FAQ.objects.all()


class ProfileView(ProfileMixin, SuccessMessageMixin, UpdateView):
    template_name = "driver/profile.html"
    user_form = UserModelForm
    model = Profile
    form_class = ProfileModelForm
    success_message = "Profile has been updated successfully"
    success_url = reverse_lazy("driver:index")


class UserChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'driver/change-password.html'
    success_url = reverse_lazy('driver:index')
    success_message = 'Your password was successfully updated!'
    form_class = PasswordChangeForm


class OrderDeliveryListView(ListView):
    template_name = "driver/order-delivery-list.html"
    context_object_name = "order_delivery_list"

    def get_queryset(self):
        queryset = OrderDelivery.objects.filter(driver=self.request.user, status="PG")
        return queryset


class InTransitOrderDeliveryListView(ListView):
    template_name = "driver/order-delivery-list.html"
    context_object_name = "order_delivery_list"

    def get_queryset(self):
        queryset = OrderDelivery.objects.filter(driver=self.request.user, status="IT")
        return queryset


class CompletedOrderDeliveryListView(ListView):
    template_name = "driver/order-delivery-list.html"
    context_object_name = "order_delivery_list"

    def get_queryset(self):
        queryset = OrderDelivery.objects.filter(driver=self.request.user, status="AR")
        return queryset


class LoanOrderDeliveryListView(ListView):
    template_name = "driver/loan-order-delivery-list.html"
    context_object_name = "loan_order_delivery_list"

    def get_queryset(self):
        queryset = LoanOrderDelivery.objects.filter(driver=self.request.user, status="PG")
        return queryset


class InTransitLoanOrderDeliveryListView(ListView):
    template_name = "driver/loan-order-delivery-list.html"
    context_object_name = "loan_order_delivery_list"

    def get_queryset(self):
        queryset = LoanOrderDelivery.objects.filter(driver=self.request.user, status="IT")
        return queryset


class CompletedLoanOrderDeliveryListView(ListView):
    template_name = "driver/loan-order-delivery-list.html"
    context_object_name = "loan_order_delivery_list"

    def get_queryset(self):
        queryset = LoanOrderDelivery.objects.filter(driver=self.request.user, status="AR")
        return queryset


def confirm_delivered_order(request, pk):
    order = get_object_or_404(OrderDelivery, pk=pk)
    order.status = "AR"
    order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def confirm_delivered_loan_order(request, pk):
    order = get_object_or_404(LoanOrderDelivery, pk=pk)
    order.status = "AR"
    order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AssignedOrdersListView(ListView):
    template_name = "driver/order-delivery-list.html"
    context_object_name = "order_delivery_list"

    def get_queryset(self):
        queryset: QuerySet[OrderDelivery] = OrderDelivery.objects.filter(driver=self.request.user)
        return queryset


class AssignedLoanOrdersListView(ListView):
    template_name = "driver/loan-order-delivery-list.html"
    context_object_name = "loan_order_delivery_list"

    def get_queryset(self):
        queryset: QuerySet[LoanOrderDelivery] = LoanOrderDelivery.objects.filter(driver=self.request.user)
        return queryset


def mark_order_delivery_status_as_in_transit(request, pk):
    instance = get_object_or_404(OrderDelivery, pk=pk)
    instance.status = "IT"
    instance.save()
    messages.success(request, "Order delivery status has been marked as in transit")
    return redirect("driver:order-delivery")


def mark_order_delivery_status_as_arrived(request, pk):
    instance = get_object_or_404(OrderDelivery, pk=pk)
    instance.status = "AR"
    instance.save()
    order = instance.order
    order.arrived = True
    order.save()
    messages.success(request, "Order delivery status has been marked as arrived")
    return redirect("driver:order-delivery")


def mark_loan_order_delivery_status_as_in_transit(request, pk):
    instance = get_object_or_404(LoanOrderDelivery, pk=pk)
    instance.status = "IT"
    instance.save()
    messages.success(request, "Loan Order delivery status has been marked as in transit")
    return redirect("driver:loan-order-delivery")


def mark_loan_order_delivery_status_as_arrived(request, pk):
    instance = get_object_or_404(LoanOrderDelivery, pk=pk)
    instance.status = "AR"
    instance.save()
    order = instance.order
    order.arrived = True
    order.save()
    messages.success(request, "Loan Order delivery status has been marked as arrived")
    return redirect("driver:loan-order-delivery")

