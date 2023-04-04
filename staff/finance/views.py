from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from loan.models import Saving
from accounts.forms import UserModelForm, ProfileModelForm, StaffFeedbackModelForm
from accounts.mixins import ProfileMixin
from accounts.models import FAQ, Profile, Feedback, DialogsModel
from client.helpers import create_dialog_
from loan.models import LoanRepaymentTransaction, LoanApplication, LoanAccount
from stock.models import OrderPayment, LoanOrderInstallments
from django.http import Http404



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


# def confirm_loan_repayment(request, pk):
#     loan_repayment_obj = get_object_or_404(LoanRepaymentTransaction, pk=pk)
#     loan_repayment_obj.confirmed = True
#     loan_repayment_obj.save()
#     messages.success(request, "Payment has been approved successfully")
#     return redirect('finance:loan-repayment-list')

from django.shortcuts import get_object_or_404, redirect


from decimal import Decimal
from django.db.models import F


def confirm_loan_repayment(request, pk):
    loan_repayment_obj = get_object_or_404(LoanRepaymentTransaction, pk=pk)
    loan_repayment_obj.confirmed = True
    loan_repayment_obj.save()
    
    # Update LoanApplication amount
    loan_application = loan_repayment_obj.repayment.loan
    loan_application.amount -= loan_repayment_obj.amount
    loan_application.save()

    # Increment Account with id=1 by the amount confirmed
    account = Account.objects.get(id=1)
    account.amount += loan_repayment_obj.amount
    account.save()

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


# def confirm_loan(request, pk):
#     loan = get_object_or_404(LoanApplication, pk=pk)
#     loan.status = "AP"
#     loan.save()
#     messages.success(request, "Loan has been approved successfully")
#     return redirect("finance:loan-list")



# def confirm_loan(request, pk):
#     loan = get_object_or_404(LoanApplication, pk=pk)
#     if loan.status != "AP":
#         loan.status = "AP"
#         loan.save()
#         try:
#             loan_account = LoanAccount.objects.get(user=loan.user)
#             loan_account.amount += loan.amount
#             loan_account.save()
#         except LoanAccount.DoesNotExist:
#             loan_account = LoanAccount.objects.create(user=loan.user, amount=loan.amount)
#         messages.success(request, "Loan has been approved successfully")
#     else:
#         messages.warning(request, "Loan is already approved")
#     return redirect("finance:loan-list")

from decimal import Decimal

def confirm_loan(request, pk):
    loan = get_object_or_404(LoanApplication, pk=pk)
    if loan.status != "AP":
        # Check if loan amount is less than account amount
        account = Account.objects.filter(id=1).first()
        if account and loan.amount <= account.amount:
            loan.status = "AP"
            loan.save()
            try:
                loan_account = LoanAccount.objects.get(user=loan.user)
                loan_account.amount += loan.amount
                loan_account.save()
            except LoanAccount.DoesNotExist:
                loan_account = LoanAccount.objects.create(user=loan.user, amount=loan.amount)
            # Deduct loan amount from MBB Sacco Account
            account.amount -= loan.amount
            account.save()
            messages.success(request, "Loan has been approved successfully")
        else:
            balance = account.amount if account else 0
            messages.warning(request, f"Loan amount exceeds available funds in MBB Sacco Account. MBB Sacco Account balance is {balance}.")
    else:
        messages.warning(request, "Loan is already approved")
    return redirect("finance:loan-list")




from django.shortcuts import redirect
from django.http import Http404
from django.db.models import F
from loan.models import Account

from djmoney.money import Money

class PendingSavingsListView(ListView):
    model = Saving
    template_name = 'finance/pending_savings.html'
    context_object_name = 'savings_list'

    def get_queryset(self):
        return super().get_queryset().filter(status=Saving.Status.PENDING)

    def post(self, request, *args, **kwargs):
        saving_id = request.POST.get('saving_id')
        if saving_id is not None:
            try:
                saving = Saving.objects.get(id=saving_id)
            except Saving.DoesNotExist:
                print('Saving does not exist')
                raise Http404('Saving not found')
            saving.status = Saving.Status.APPROVED
            saving.save()

            # Get or create Account instance and increment its amount by the approved savings amount
            account, created = Account.objects.get_or_create(id=1)
            account.amount += saving.amount
            account.save()

        return redirect(request.path)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['saving_id'] = self.request.POST.get('saving_id')
        return context

from django.shortcuts import render
from loan.models import Account



def account_total_view(request):
    account = Account.objects.get(id=1)  # Assuming the account ID is always 1
    context = {'account': account}
    return render(request, 'finance/account_total.html', context)



class ApprovedSavingsListView(ListView):
    model = Saving
    template_name = 'finance/approved_savings.html'
    context_object_name = 'savings_list'

    def get_queryset(self):
        return super().get_queryset().filter(status=Saving.Status.APPROVED)