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
from client.helpers import add_to_cart_functionality, remove_from_cart_functionality, delete_item_cart_functionality, \
    get_cart_total_amount, keeping_track_of_bought_products, create_dialog_
from delivery.forms import UserPickUpStationModelForm
from delivery.models import UserPickUpStation, OrderDelivery, LoanOrderDelivery
from stock.forms import OrderPaymentModelForm
from stock.mixins import CartMixin, GeneratePdfMixin
from stock.models import Product, Order, OrderPayment


class DashboardView(CartMixin, TemplateView):
    template_name = 'customer/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user, complete=True)
        context['product_list'] = Product.objects.all()
        return context


class ProductDetailView(CartMixin, DetailView):
    template_name = 'customer/product-detail.html'
    model = Product


class AddToCartView(View):
    def get(self, *args, **kwargs):
        add_to_cart_functionality(self)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', reverse_lazy("customer:index")))


class RemoveFromCartView(View):
    def get(self, *args, **kwargs):
        remove_from_cart_functionality(self)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', reverse_lazy("customer:cart-list")))


class DeleteItemFromCartView(View):
    def get(self, *args, **kwargs):
        delete_item_cart_functionality(self)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', reverse_lazy("customer:cart-list")))


class OrderListView(CartMixin, ListView):
    template_name = "customer/order-list.html"
    context_object_name = "order_list"

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class OrderPaymentListView(CartMixin, ListView):
    template_name = "customer/order-payment-list.html"
    context_object_name = "order_payment_list"

    def get_queryset(self):
        queryset = OrderPayment.objects.filter(order__user=self.request.user)
        return queryset


class ProductListView(CartMixin, ListView):
    template_name = "customer/product-list.html"
    context_object_name = "product_list"

    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset


class FAQListView(CartMixin, ListView):
    template_name = "customer/faq.html"

    def get_queryset(self):
        return FAQ.objects.all()


class ProfileView(CartMixin, ProfileMixin, SuccessMessageMixin, UpdateView):
    template_name = "customer/profile.html"
    user_form = UserModelForm
    model = Profile
    form_class = ProfileModelForm
    success_message = "Profile has been updated successfully"
    success_url = reverse_lazy("customer:index")


class UserChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'customer/change-password.html'
    success_url = reverse_lazy('customer:index')
    success_message = 'Your password was successfully updated!'
    form_class = PasswordChangeForm


class SearchView(CartMixin, TemplateView):
    template_name = "customer/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            search = self.request.GET.get("search")
            context['product_list'] = Product.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search))
            context['search'] = search
        return context


class CartListView(CartMixin, TemplateView):
    template_name = "customer/cart-list.html"


class CheckoutView(CartMixin, SuccessMessageMixin, CreateView):
    model = OrderPayment
    form_class = OrderPaymentModelForm
    template_name = "customer/checkout.html"
    success_message = "your payment has been sent successfully"
    success_url = reverse_lazy('customer:index')

    def form_valid(self, form):
        instance = form.save(commit=False)
        cart = self.get_context_data()['cart']
        instance.amount = get_cart_total_amount(cart.order_items.all())
        instance.order = cart
        keeping_track_of_bought_products(cart=cart)
        cart.complete = True
        cart.save()
        return super().form_valid(form)


class OrderPdfView(GeneratePdfMixin, View):
    pdf_template = "customer/receipts/order-pdf.html"

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
    pdf_template = "customer/receipts/order-payment-pdf.html"

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


class PickUpStationView(CartMixin, SuccessMessageMixin, UserFormKwargsMixin, CreateView):
    template_name = "customer/pickup-station.html"
    form_class = UserPickUpStationModelForm
    model = UserPickUpStation
    success_message = "you selected a pickup station successfully."
    success_url = reverse_lazy("customer:selected-pickup-station")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)


class PickUpStationUpdateView(CartMixin, SuccessMessageMixin, UserFormKwargsMixin, UpdateView):
    template_name = "customer/pickup-station.html"
    form_class = UserPickUpStationModelForm
    model = UserPickUpStation
    success_message = "you selected a pickup station successfully."
    success_url = reverse_lazy("customer:selected-pickup-station")


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
    template_name = "customer/selected-pickup-station.html"
    context_object_name = "selected_pickup_station_list"

    def get_queryset(self):
        queryset = UserPickUpStation.objects.filter(user=self.request.user)
        return queryset


class OrderDeliveryListView(ListView):
    template_name = "customer/order-delivery-list.html"
    context_object_name = "order_delivery_list"

    def get_queryset(self):
        queryset = OrderDelivery.objects.filter(order__user=self.request.user, picked=False)
        return queryset


def select_pickup_station(request, pk):
    station = get_object_or_404(UserPickUpStation, pk=pk)
    UserPickUpStation.objects.filter(user=request.user).update(selected=False)
    station.selected = True
    station.save()
    messages.success(request, "Station has been selected successfully.")
    return redirect("customer:cart-list")


class OrderDeliveryDetailView(View):
    template_name = "customer/order-delivery-detail.html"

    def get(self, *args, **kwargs):
        order_delivery = OrderDelivery.objects.filter(order_id=self.kwargs.get("pk")).first()
        return render(self.request, self.template_name, {"order_delivery": order_delivery})


class LoanOrderDeliveryDetailView(View):
    template_name = "customer/loan-order-delivery-detail.html"

    def get(self, *args, **kwargs):
        order_delivery = LoanOrderDelivery.objects.filter(order_id=self.kwargs.get("pk")).first()
        return render(self.request, self.template_name, {"order_delivery": order_delivery})


class FeedbackCreateView(CartMixin, SuccessMessageMixin, CreateView):
    template_name = "customer/feedback.html"
    form_class = FeedbackModelForm
    model = Feedback
    success_message = "feedback has been sent successfully"
    success_url = reverse_lazy("customer:feedback")

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
    return redirect("customer:index")
