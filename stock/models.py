from _decimal import Decimal

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _
from djmoney.money import Money

from core.utils import TimeStampModel, generate_key

User: AbstractUser = get_user_model()


class Category(TimeStampModel):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return str(self.name)


class Product(TimeStampModel):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    description = RichTextUploadingField(_('content'))
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/%Y/%m/', default="products/default.png")

    class Meta:
        unique_together = ['name', 'category']

    def __str__(self):
        return str(self.name)


class ProductLoan(TimeStampModel):
    class LoanDuration(models.TextChoices):
        ONE_YEAR = 'OY', _('One Year')
        TWO_YEARS = 'TY', _('Two Years')
        THREE_YEARS = 'THY', _('Three Years')

    class InterestRates(models.TextChoices):
        THREE_PERCENT = 1.03, _('3 %')
        FIVE_PERCENT = 1.05, _('5 %')
        SEVEN_PERCENT = 1.07, _('7 %')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    duration = models.CharField(max_length=5, choices=LoanDuration.choices, default=LoanDuration.ONE_YEAR)
    interest_rate = models.FloatField(choices=InterestRates.choices, default=InterestRates.THREE_PERCENT)

    def save(self, *args, **kwargs):
        if self.duration == "OY":
            self.interest_rate = self.InterestRates.THREE_PERCENT
        elif self.duration == "TY":
            self.interest_rate = self.InterestRates.FIVE_PERCENT
        elif self.duration == "THY":
            self.interest_rate = self.InterestRates.SEVEN_PERCENT
        super(ProductLoan, self).save(*args, **kwargs)

    def monthly_installment(self):
        total_amount = self.product.amount.amount * Decimal(self.interest_rate)
        deposit = total_amount * Decimal(0.2)
        total_amount -= deposit
        monthly_amount = Decimal(0.0)
        if self.duration == "OY":
            monthly_amount = total_amount / 12
        elif self.duration == "TY":
            monthly_amount = total_amount / 24
        elif self.duration == "THY":
            monthly_amount = total_amount / 36
        return Money(monthly_amount, 'KES')

    def installment_count(self):
        count: int = 0
        if self.duration == "OY":
            count = 12
        elif self.duration == "TY":
            count = 24
        elif self.duration == "THY":
            count = 36
        return count

    def total_amount(self):
        print(Decimal(self.interest_rate))
        total_amount = self.product.amount.amount * Decimal(self.interest_rate)
        return Money(total_amount, 'KES')

    def get_deposit(self):
        total_amount = self.product.amount.amount * Decimal(self.interest_rate)
        deposit = total_amount * Decimal(0.2)
        return Money(deposit, 'KES')


class Order(TimeStampModel):
    transaction_id = models.CharField(max_length=250, default=generate_key(9, 9))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    complete = models.BooleanField(default=False)
    assigned = models.BooleanField(default=False)
    arrived = models.BooleanField(default=False)

    def get_total_items(self):
        order_items = self.order_items.all()
        total_items: int = 0
        for order_item in order_items:
            total_items += order_item.quantity
        return total_items

    def get_total_amount(self):
        order_items = self.order_items.all()
        total_amount = 0
        for order_item in order_items:
            total_amount += order_item.product.amount.amount * order_item.quantity
        return Money(total_amount, 'KES')


class OrderItem(TimeStampModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.IntegerField(default=0)

    def total(self):
        total_amount = self.quantity * self.product.amount.amount
        return Money(total_amount, 'KES')


class LoanOrder(TimeStampModel):
    transaction_id = models.CharField(max_length=250, default=generate_key(9, 9))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loan_orders")
    product_loan = models.ForeignKey(ProductLoan, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    assigned = models.BooleanField(default=False)
    arrived = models.BooleanField(default=False)

    def get_remaining_amount(self):
        loan_order_installments = self.loan_order_installments.all()
        paid_amount = Decimal(0.0)
        for installment in loan_order_installments:
            paid_amount += installment.amount.amount
        remaining_amount = self.product_loan.total_amount().amount - paid_amount
        return Money(remaining_amount, "KES")

    def deposit_paid(self):
        paid = False
        for payment in self.loan_order_installments:
            if payment.type == "DP":
                paid = True
        return paid


class OrderPaymentAbstract(TimeStampModel):
    transaction_id = models.CharField(max_length=250, default=generate_key(9, 9))
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    mpesa_code = models.CharField(max_length=10)
    confirm = models.BooleanField(default=False)

    class Meta:
        abstract = True


class LoanOrderInstallments(OrderPaymentAbstract):
    class InstallmentType(models.TextChoices):
        DEPOSIT = 'DP', _('Deposit')
        MONTHLY_INSTALLMENTS = 'MI', _('Monthly Installments')

    order = models.ForeignKey(LoanOrder, on_delete=models.CASCADE, related_name="loan_order_installments")
    type = models.CharField(max_length=2, choices=InstallmentType.choices, default=InstallmentType.DEPOSIT)


class OrderPayment(OrderPaymentAbstract):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
