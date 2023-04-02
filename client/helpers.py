from typing import Optional

from django.contrib import messages
from django.shortcuts import get_object_or_404

from accounts.models import User, DialogsModel
from stock.helpers import get_cart
from stock.models import OrderItem, LoanOrder


def add_to_cart_functionality(self):
    product_id = self.kwargs.get('product_id')
    order = get_cart(self.request.user)
    if OrderItem.objects.filter(order=order, product_id=product_id).exists():
        order_item = get_object_or_404(OrderItem, order=order, product_id=product_id)
        if order_item.quantity >= order_item.product.quantity:
            messages.info(self.request, f"sorry only {order_item.product.quantity} {order_item.product.name} "
                                        f"are remaining")
        else:
            if order_item.product.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.success(self.request, "product quantity has been incremented successfully")
            else:
                messages.info(self.request, f"Sorry product is out of stock")
    else:
        item, created = OrderItem.objects.get_or_create(order=order, product_id=product_id)
        item.quantity = 1
        item.save()
        messages.success(self.request, "product has been added successfully to cart")


def remove_from_cart_functionality(self):
    product_id = self.kwargs.get('product_id')
    order = get_cart(self.request.user)
    if OrderItem.objects.filter(order=order, product_id=product_id).exists():
        order_item = get_object_or_404(OrderItem, order=order, product_id=product_id)
        if order_item.quantity >= 1:
            order_item.quantity -= 1
            order_item.save()
            messages.success(self.request, "product has been removed from cart successfully")
        else:
            messages.success(self.request, "product has been cleared from cart successfully")
    else:
        messages.info(self.request, "sorry, product does not exist in cart")


def delete_item_cart_functionality(self):
    product_id = self.kwargs.get('product_id')
    order = get_cart(self.request.user)
    if OrderItem.objects.filter(order=order, product_id=product_id).exists():
        order_item = get_object_or_404(OrderItem, order=order, product_id=product_id)
        order_item.delete()
        messages.success(self.request, "product has been cleared from cart successfully")
    else:
        messages.info(self.request, "sorry, product does not exist in cart")


def keeping_track_of_bought_products(cart):
    order_items = cart.order_items.all()
    for item in order_items:
        product = item.product
        product.quantity -= item.quantity
        product.save()


def get_cart_total_amount(order_items):
    total_amount = 0
    for order_item in order_items:
        total_amount += order_item.product.amount.amount * order_item.quantity
    return total_amount


def calculate_remaining_loan(user):
    if LoanOrder.objects.filter(user=user, complete=False).exists():
        loan_order = LoanOrder.objects.filter(user=user, complete=False).first()
    return loan_order


def get_staff_id_(feedback_type: str) -> int:
    match feedback_type:
        case "CST_FMR":
            user_id = User.objects.filter(type="FM").last().pk
        case "CST_SMR":
            user_id = User.objects.filter(type="SM").last().pk
        case _:
            user_id = None
    return user_id


def create_dialog_(user_id: int, feedback_type: str, staff_id: Optional[int] = None) -> int:
    if not staff_id:
        staff_id = get_staff_id_(feedback_type=feedback_type)
    dialog, created = DialogsModel.objects.get_or_create(customer_id=user_id, staff_id=staff_id)
    return dialog.pk

