from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView

from accounts.forms import UserModelForm, ProfileModelForm, StaffFeedbackModelForm
from accounts.mixins import ProfileMixin
from accounts.models import FAQ, Profile, Feedback, DialogsModel
from client.helpers import create_dialog_
from loan.models import LoanRepaymentTransaction, LoanApplication
from stock.models import OrderPayment, LoanOrderInstallments


class DashboardView(TemplateView):
    template_name = "finance/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_loan_order'] = LoanOrderInstallments.objects.filter(confirm=False)
        context['pending_order'] = OrderPayment.objects.filter(confirm=False)
        context['pending_loan'] = LoanRepaymentTransaction.objects.filter(confirmed=False)
        return context


class LoanRepaymentList(ListView):
    template_name = "finance/loan-repayment-list.html"
    context_object_name = "loan_repayment_list"

    def get_queryset(self):
        queryset = LoanRepaymentTransaction.objects.filter(confirmed=False)
        return queryset


class ApprovedLoanRepaymentList(ListView):
    template_name = "finance/loan-repayment-list.html"
    context_object_name = "loan_repayment_list"

    def get_queryset(self):
        queryset = LoanRepaymentTransaction.objects.filter(confirmed=True)
        return queryset


class OrderPaymentList(ListView):
    template_name = "finance/order-payment-list.html"
    context_object_name = "order_payment_list"

    def get_queryset(self):
        queryset = OrderPayment.objects.filter(confirm=False)
        return queryset


class ApprovedOrderPaymentList(ListView):
    template_name = "finance/order-payment-list.html"
    context_object_name = "order_payment_list"

    def get_queryset(self):
        queryset = OrderPayment.objects.filter(confirm=True)
        return queryset


class LoanOrderPaymentList(ListView):
    template_name = "finance/loan-order-payment-list.html"
    context_object_name = "loan_order_payment_list"

    def get_queryset(self):
        queryset = LoanOrderInstallments.objects.filter(confirm=False)
        return queryset


class ApprovedLoanOrderPaymentList(ListView):
    template_name = "finance/loan-order-payment-list.html"
    context_object_name = "loan_order_payment_list"

    def get_queryset(self):
        queryset = LoanOrderInstallments.objects.filter(confirm=True)
        return queryset


def confirm_loan_repayment(request, pk):
    loan_repayment_obj = get_object_or_404(LoanRepaymentTransaction, pk=pk)
    loan_repayment_obj.confirmed = True
    loan_repayment_obj.save()
    messages.success(request, "Payment has been approved successfully")
    return redirect('finance:loan-repayment-list')


def confirm_order_payment(request, pk):
    order_payment = get_object_or_404(OrderPayment, pk=pk)
    order_payment.confirm = True
    order_payment.save()
    messages.success(request, "Payment has been approved successfully")
    return redirect('finance:order-payment-list')


def confirm_loan_order_payment(request, pk):
    loan_order_payment = get_object_or_404(LoanOrderInstallments, pk=pk)
    loan_order_payment.confirm = True
    loan_order_payment.save()
    messages.success(request, "Payment has been approved successfully")
    return redirect('finance:loan-order-payment-list')


class FAQListView(ListView):
    template_name = "finance/faq.html"

    def get_queryset(self):
        return FAQ.objects.all()


class ProfileView(ProfileMixin, SuccessMessageMixin, UpdateView):
    template_name = "finance/profile.html"
    user_form = UserModelForm
    model = Profile
    form_class = ProfileModelForm
    success_message = "Profile has been updated successfully"
    success_url = reverse_lazy("finance:index")


class UserChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'finance/change-password.html'
    success_url = reverse_lazy('finance:index')
    success_message = 'Your password was successfully updated!'
    form_class = PasswordChangeForm


class FeedbackCreateView(SuccessMessageMixin, CreateView):
    template_name = "finance/feedback.html"
    form_class = StaffFeedbackModelForm
    model = Feedback
    success_message = "feedback has been sent successfully"

    def get_success_url(self):
        return reverse_lazy("finance:customer-feedback", kwargs=dict(customer_id=self.kwargs.get("customer_id")))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedback_list'] = Feedback.objects.filter(
            Q(type="CST_FMR") | Q(type="FMR_CST"),
            dialog__customer_id=self.kwargs.get("customer_id"),
        ).order_by("created")
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.dialog_id = create_dialog_(
            user_id=self.kwargs.get("customer_id"), feedback_type=instance.type, staff_id=self.request.user.pk
        )
        instance.type = "FMR_CST"
        return super().form_valid(form)


class FeedbackListView(ListView):
    template_name = "finance/feedback-list.html"
    context_object_name = "dialog_list"

    def get_queryset(self):
        return DialogsModel.objects.filter(staff__type="FM")


class LoanApplicationListView(ListView):
    template_name = "finance/loan-list.html"
    context_object_name = "loan_list"

    def get_queryset(self):
        return LoanApplication.objects.all().order_by("-created")


def confirm_loan(request, pk):
    loan = get_object_or_404(LoanApplication, pk=pk)
    loan.status = "AP"
    loan.save()
    messages.success(request, "Loan has been approved successfully")
    return redirect("finance:loan-list")
