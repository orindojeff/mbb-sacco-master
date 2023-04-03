from braces.views import UserFormKwargsMixin
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DetailView

from accounts.forms import UserModelForm, ProfileModelForm, FeedbackModelForm
from accounts.mixins import ProfileMixin
from accounts.models import FAQ, Profile, Feedback
from client.helpers import add_to_cart_functionality, remove_from_cart_functionality, delete_item_cart_functionality, \
    keeping_track_of_bought_products, get_cart_total_amount, create_dialog_
from delivery.forms import UserPickUpStationModelForm
from delivery.models import UserPickUpStation, OrderDelivery, LoanOrderDelivery
from loan.forms import LoanApplicationModelForm, LoanRepaymentTransactionModelForm, SavingTransactionModelForm, \
    SavingsWithdrawalModelForm
from loan.models import LoanApplication, LoanRepaymentTransaction, Saving, SavingTransaction, SavingsWithdrawal
from stock.forms import OrderPaymentModelForm, RiderProductLoanModelForm, LoanOrderInstallmentsModelForm
from stock.mixins import CartMixin, GeneratePdfMixin
from stock.models import Product, Order, OrderPayment, ProductLoan, LoanOrder, LoanOrderInstallments
from loan.models import LoanAccount

class DashboardView(CartMixin, TemplateView):
    template_name = 'rider/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        savings, created = Saving.objects.get_or_create(user=self.request.user)
        context['orders'] = Order.objects.filter(user=self.request.user, complete=True)
        context['order_delivery'] = OrderDelivery.objects.filter(order__user=self.request.user, picked=False)
        context['loan_order_delivery'] = LoanOrderDelivery.objects.filter(order__user=self.request.user, picked=False)

        # loan account
        loan_accounts = LoanAccount.objects.filter(user=self.request.user)
        context['loan_account'] = loan_accounts
        context['total_loan_amount'] = sum([loan_account.amount for loan_account in loan_accounts])
        
        # Add savings data to the context
        context['pending_savings'] = savings.amount if savings.status == Saving.Status.PENDING else 0
        context['approved_savings'] = savings.amount if savings.status == Saving.Status.APPROVED else 0

        return context


class AppliedLoanListView(CartMixin, ListView):
    template_name = "rider/applied-loan-list.html"
    context_object_name = "loan_list"

    def get_queryset(self):
        queryset = LoanApplication.objects.filter(user=self.request.user)
        return queryset


class SavingView(CartMixin, SuccessMessageMixin, CreateView):
    model = SavingTransaction
    form_class = SavingTransactionModelForm
    template_name = "rider/saving-transaction.html"
    success_url = reverse_lazy("rider:index")
    success_message = "Your savings has been sent successfully"

    def form_valid(self, form):
        instance = form.save(commit=False)
        saving, created = Saving.objects.get_or_create(user=self.request.user)
        instance.saving = saving
        return super().form_valid(form)


class LoanApplyView(CartMixin, UserFormKwargsMixin, SuccessMessageMixin, CreateView):
    model = LoanApplication
    form_class = LoanApplicationModelForm
    template_name = "rider/loan-application.html"
    success_url = reverse_lazy("rider:index")
    success_message = "Your application has been sent successfully"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)


from decimal import Decimal


class LoanRepaymentView(CartMixin, SuccessMessageMixin, CreateView):
    model = LoanRepaymentTransaction
    form_class = LoanRepaymentTransactionModelForm
    template_name = "rider/loan-repayment.html"
    success_url = reverse_lazy("rider:index")
    success_message = "You're loan payment has been sent successfully"

    def form_valid(self, form):
        instance = form.save(commit=False)
        repayment = instance.repayment
        repayment.paid = True
        repayment.save()
        return super().form_valid(form)


# from django.contrib.messages.views import SuccessMessageMixin
# from django.urls import reverse_lazy
# from django.views.generic import CreateView


# class LoanRepaymentView(CartMixin, SuccessMessageMixin, UserFormKwargsMixin, CreateView):
#     template_name = 'rider/loan-repayment.html'
#     form_class = LoanRepaymentTransactionModelForm
#     success_url = reverse_lazy('loan_repayment_success')
#     success_message = 'Loan repayment transaction has been submitted successfully'

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user # pass the user to the form
#         repayment_id = self.request.GET.get('repayment_id')
#         if repayment_id:
#             repayment = LoanRepayment.objects.get(id=repayment_id)
#             kwargs['instance'] = LoanRepaymentTransaction(repayment=repayment)
#         return kwargs

#     def form_valid(self, form):
#         transaction = form.save()
#         repayment = transaction.repayment
#         # Update LoanRepayment's min_repayment field with the calculated minimum repayment
#         repayment.min_repayment = repayment.calculate_min_repayment()
#         repayment.save()
#         return super().form_valid(form)






class LoanRepaymentListView(CartMixin, ListView):
    template_name = "rider/loan-repayment-list.html"
    context_object_name = "loan_repayment_list"

    def get_queryset(self):
        queryset = LoanRepaymentTransaction.objects.filter(repayment__loan__user=self.request.user)
        return queryset


class OrderListView(CartMixin, ListView):
    template_name = "rider/order-list.html"
    context_object_name = "order_list"

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class OrderPaymentListView(CartMixin, ListView):
    template_name = "rider/order-payment-list.html"
    context_object_name = "order_payment_list"

    def get_queryset(self):
        queryset = OrderPayment.objects.filter(order__user=self.request.user)
        return queryset


class ProductListView(CartMixin, ListView):
    template_name = "rider/product-list.html"
    context_object_name = "product_list"

    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset


class FAQListView(CartMixin, ListView):
    template_name = "rider/faq.html"

    def get_queryset(self):
        return FAQ.objects.all()


class ProfileView(CartMixin, ProfileMixin, SuccessMessageMixin, UpdateView):
    template_name = "rider/profile.html"
    user_form = UserModelForm
    model = Profile
    form_class = ProfileModelForm
    success_message = "Profile has been updated successfully"
    success_url = reverse_lazy("rider:index")


class UserChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'rider/change-password.html'
    success_url = reverse_lazy('rider:index')
    success_message = 'Your password was successfully updated!'
    form_class = PasswordChangeForm


class OrderPdfView(GeneratePdfMixin, View):
    pdf_template = "rider/receipts/order-pdf.html"

    def get_object(self):
        order = get_object_or_404(Order, pk=self.kwargs.get("pk"))
        return order

    def get_pdf_name(self):
        super().get_pdf_name()
        return f"order-{self.get_object().transaction_id}"

    def get_pdf_data(self):
        super().get_pdf_data()
        return {"order": self.get_object()}

    def get(self, *args, **kwargs):
        return self.generate_pdf()


class OrderPaymentPdfView(GeneratePdfMixin, View):
    pdf_template = "rider/receipts/order-payment-pdf.html"

    def get_object(self):
        order = get_object_or_404(OrderPayment, pk=self.kwargs.get("pk"))
        return order

    def get_pdf_name(self):
        super().get_pdf_name()
        return f"order-{self.get_object().transaction_id}"

    def get_pdf_data(self):
        super().get_pdf_data()
        return {"payment": self.get_object()}

    def get(self, *args, **kwargs):
        return self.generate_pdf()


class AddToCartView(View):
    def get(self, *args, **kwargs):
        add_to_cart_functionality(self)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', reverse_lazy("rider:product-list")))


class RemoveFromCartView(View):
    def get(self, *args, **kwargs):
        remove_from_cart_functionality(self)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', reverse_lazy("rider:cart-list")))


class DeleteItemFromCartView(View):
    def get(self, *args, **kwargs):
        delete_item_cart_functionality(self)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', reverse_lazy("rider:cart-list")))


class CartListView(CartMixin, TemplateView):
    template_name = "rider/cart-list.html"


class CheckoutView(CartMixin, SuccessMessageMixin, CreateView):
    model = OrderPayment
    form_class = OrderPaymentModelForm
    template_name = "rider/checkout.html"
    success_message = "your payment has been sent successfully"
    success_url = reverse_lazy('rider:index')

    def form_valid(self, form):
        instance = form.save(commit=False)
        cart = self.get_context_data()['cart']
        instance.amount = get_cart_total_amount(cart.order_items.all())
        instance.order = cart
        keeping_track_of_bought_products(cart=cart)
        cart.complete = True
        cart.save()
        if UserPickUpStation.objects.filter(user=self.request.user).exists():
            station = UserPickUpStation.objects.filter(user=self.request.user).last()
            OrderDelivery.objects.get_or_create(order=cart, station=station)
        return super().form_valid(form)




class ProductLoanView(CartMixin, TemplateView):
    form_class = RiderProductLoanModelForm
    template_name = "rider/product-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['product_list'] = Product.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            product_id = kwargs.get('product_id')
            product_loan = get_object_or_404(ProductLoan, product_id=product_id, duration=instance.duration)
            if not LoanOrder.objects.filter(user=request.user, complete=False).exists():
                loan_order = LoanOrder.objects.create(user=request.user, product_loan=product_loan, complete=False)
                messages.success(request, "Order has been sent successfully")
                return redirect('rider:product-loan-checkout', pk=loan_order.pk)
            else:
                messages.info(request, "Sorry, you have an existing product loan")
        else:
            messages.error(request, "Failed to send order")
        return redirect('rider:product-loan-checkout', kwargs={'pk': ProductLoan.pk})


class ProductLoanOrderListView(CartMixin, ListView):
    # TODO: fix the error with filter bro
    template_name = "rider/product-loan-order-list.html"
    context_object_name = "product_loan_order_list"

    def get_queryset(self):
        queryset = LoanOrder.objects.filter(user=self.request.user, complete=False)
        return queryset


class ProductLoanCheckoutView(CartMixin, SuccessMessageMixin, CreateView):
    template_name = "rider/product-loan-checkout.html"
    model = LoanOrderInstallments
    form_class = LoanOrderInstallmentsModelForm
    success_message = "Deposit has been sent successfully"
    success_url = reverse_lazy('rider:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loan_order = get_object_or_404(LoanOrder, pk=self.kwargs.get('pk'))
        context['loan_order'] = loan_order
        return context

    def form_valid(self, form):
        loan_order = self.get_context_data()['loan_order']
        instance = form.save(commit=False)
        instance.order = loan_order
        instance.type = "DP"
        instance.amount = loan_order.product_loan.get_deposit()
        instance.save()
        if loan_order.product_loan.installment_count() == loan_order.product_loan.duration:

            loan_order.complete = True
            loan_order.save()
            messages.success(self.request, "Loan order has been completed successfully")
        return super().form_valid(form)



class ProductLoanPaymentListView(CartMixin, ListView):
    template_name = "rider/product-loan-payment-list.html"
    context_object_name = "product_loan_payment_list"

    def get_queryset(self):
        queryset = LoanOrderInstallments.objects.filter(order__user=self.request.user)
        return queryset


class SearchView(CartMixin, TemplateView):
    template_name = "rider/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            search = self.request.GET.get("search")
            context['product_list'] = Product.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search))
            context['search'] = search
        return context


class ProductDetailView(CartMixin, DetailView):
    model = Product
    template_name = "rider/product-detail.html"
    context_object_name = "product"


class PayProductLoanView(CartMixin, SuccessMessageMixin, CreateView):
    template_name = "rider/pay-product-loan.html"
    model = LoanOrderInstallments
    form_class = LoanOrderInstallmentsModelForm
    success_message = "Monthly Installment has been sent successfully"
    success_url = reverse_lazy('rider:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loan_order'] = LoanOrder.objects.filter(user=self.request.user, complete=False).first()
        return context

    def form_valid(self, form):
        loan_order = self.get_context_data()['loan_order']
        instance = form.save(commit=False)
        instance.order = loan_order
        instance.type = "MI"
        instance.amount = loan_order.product_loan.monthly_installment()
        if loan_order.get_remaining_amount().amount < 1:
            loan_order.complete = True
            loan_order.save()
        return super().form_valid(form)


class PickUpStationView(CartMixin, SuccessMessageMixin, UserFormKwargsMixin, CreateView):
    template_name = "rider/pickup-station.html"
    form_class = UserPickUpStationModelForm
    model = UserPickUpStation
    success_message = "you selected a pickup station successfully."
    success_url = reverse_lazy("rider:selected-pickup-station")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)


class PickUpStationUpdateView(CartMixin, SuccessMessageMixin, UserFormKwargsMixin, UpdateView):
    template_name = "rider/pickup-station.html"
    form_class = UserPickUpStationModelForm
    model = UserPickUpStation
    success_message = "you selected a pickup station successfully."
    success_url = reverse_lazy("rider:selected-pickup-station")


def pick_order(request, pk):
    delivery_order = get_object_or_404(OrderDelivery, pk=pk)
    delivery_order.picked = True
    delivery_order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def pick_loan_order(request, pk):
    delivery_order = get_object_or_404(LoanOrderDelivery, pk=pk)
    delivery_order.picked = True
    delivery_order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SelectedPickUpStationListView(ListView):
    template_name = "rider/selected-pickup-station.html"
    context_object_name = "selected_pickup_station_list"

    def get_queryset(self):
        queryset = UserPickUpStation.objects.filter(user=self.request.user)
        return queryset


class OrderDeliveryListView(ListView):
    template_name = "rider/order-delivery-list.html"
    context_object_name = "order_delivery_list"

    def get_queryset(self):
        queryset = OrderDelivery.objects.filter(order__user=self.request.user, picked=False)
        return queryset


class LoanOrderDeliveryListView(ListView):
    template_name = "rider/loan-order-delivery-list.html"
    context_object_name = "order_delivery_list"

    def get_queryset(self):
        queryset = LoanOrderDelivery.objects.filter(order__user=self.request.user, picked=False)
        return queryset


def select_pickup_station(request, pk):
    station = get_object_or_404(UserPickUpStation, pk=pk)
    UserPickUpStation.objects.filter(user=request.user).update(selected=False)
    station.selected = True
    station.save()
    messages.success(request, "Station has been selected successfully.")
    return redirect("rider:cart-list")


class OrderDeliveryDetailView(View):
    template_name = "rider/order-delivery-detail.html"

    def get(self, *args, **kwargs):
        print(self.kwargs.get("pk"))
        order_delivery = OrderDelivery.objects.filter(order_id=self.kwargs.get("pk")).first()
        print(order_delivery)
        return render(self.request, self.template_name, {"order_delivery": order_delivery})


class LoanOrderDeliveryDetailView(View):
    template_name = "rider/loan-order-delivery-detail.html"

    def get(self, *args, **kwargs):
        order_delivery = LoanOrderDelivery.objects.filter(order_id=self.kwargs.get("pk")).first()
        return render(self.request, self.template_name, {"order_delivery": order_delivery})


# class SavingsWithdrawalCreateView(SuccessMessageMixin, UserFormKwargsMixin, CreateView):
#     template_name = "rider/savings-withdrawal.html"
#     form_class = SavingsWithdrawalModelForm
#     model = SavingsWithdrawal
#     success_message = "You've withdrawn successfully"
#     success_url = reverse_lazy("rider:index")

#     def form_valid(self, form):
#         instance = form.save(commit=False)
#         instance.user = self.request.user
#         return super().form_valid(form)



class SavingsWithdrawalCreateView(SuccessMessageMixin, UserFormKwargsMixin, CreateView):
    template_name = "rider/savings-withdrawal.html"
    form_class = SavingsWithdrawalModelForm
    model = SavingsWithdrawal
    success_message = "You've withdrawn successfully"
    success_url = reverse_lazy("rider:index")

    def form_valid(self, form):
        withdrawal_amount = form.cleaned_data['amount']
        loan_application = LoanAccount.objects.filter(user=self.request.user).first()
        if loan_application is not None:
            loan_application.amount -= withdrawal_amount
            loan_application.save()
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect(self.success_url)



class FeedbackCreateView(CartMixin, SuccessMessageMixin, CreateView):
    template_name = "rider/feedback.html"
    form_class = FeedbackModelForm
    model = Feedback
    success_message = "feedback has been sent successfully"
    success_url = reverse_lazy("rider:feedback")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedback_list'] = Feedback.objects.filter(dialog__customer=self.request.user).order_by("created")
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.dialog_id = create_dialog_(user_id=self.request.user.pk, feedback_type=instance.type)
        return super().form_valid(form)


def confirm_order_picked(request, pk):
    order = get_object_or_404(OrderDelivery, pk=pk)
    order.picked = True
    order.save()
    messages.success(request, "Order has been marked as picked successfully.")
    return redirect("rider:index")
