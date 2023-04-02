import re

from django.core.exceptions import ValidationError
from django.forms import ModelForm, ModelChoiceField, Form, CharField

from accounts.mixins import StyleFormMixin
from loan.models import LoanRepaymentTransaction, SavingTransaction
from stock.models import Category, Product, ProductLoan, LoanOrderInstallments, OrderPayment


class CategoryModelForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name.lower()


class ProductModelForm(StyleFormMixin, ModelForm):
    category = ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category")

    class Meta:
        model = Product
        fields = ['name', 'category', 'amount', 'description', 'quantity', 'image']


class ProductLoanModelForm(StyleFormMixin, ModelForm):
    product = ModelChoiceField(queryset=Product.objects.all(), empty_label="Select Category")

    class Meta:
        model = ProductLoan
        fields = ['product', 'duration']


class RiderProductLoanModelForm(StyleFormMixin, ModelForm):
    class Meta:
        model = ProductLoan
        fields = ['duration']


class OrderPaymentModelForm(StyleFormMixin, ModelForm):
    class Meta:
        model = OrderPayment
        fields = ['mpesa_code']

    def clean_mpesa_code(self):
        mpesa = self.cleaned_data.get('mpesa_code')
        pattern = re.compile(r"^[A-Za-z][a-zA-Z0-9]{9}")
        if not pattern.match(mpesa):
            raise ValidationError("Enter a valid Mpesa Code")
        if LoanOrderInstallments.objects.filter(mpesa_code=mpesa).exists() or \
                OrderPayment.objects.filter(mpesa_code=mpesa).exists() or \
                LoanRepaymentTransaction.objects.filter(mpesa_code=mpesa).exists() or \
                SavingTransaction.objects.filter(mpesa_code=mpesa).exists():
            raise ValidationError("Mpesa Code already used.")
        return mpesa.upper()


class LoanOrderInstallmentsModelForm(StyleFormMixin, ModelForm):
    class Meta:
        model = LoanOrderInstallments
        fields = ['mpesa_code']

    def clean_mpesa_code(self):
        mpesa = self.cleaned_data.get('mpesa_code')
        pattern = re.compile(r"^[A-Za-z][a-zA-Z0-9]{9}")
        if not pattern.match(mpesa):
            raise ValidationError("Enter a valid Mpesa Code")
        if LoanOrderInstallments.objects.filter(mpesa_code=mpesa).exists() or \
                OrderPayment.objects.filter(mpesa_code=mpesa).exists() or \
                LoanRepaymentTransaction.objects.filter(mpesa_code=mpesa).exists() or \
                SavingTransaction.objects.filter(mpesa_code=mpesa).exists():
            raise ValidationError("Mpesa Code already used.")
        return mpesa.upper()


class MpesaForm(StyleFormMixin, Form):
    mpesa = CharField(max_length=10, empty_value="Mpesa")

    def clean_mpesa(self):
        mpesa = self.cleaned_data.get('mpesa')
        pattern = re.compile(r"^[A-Za-z][a-zA-Z0-9]{9}")
        if not pattern.match(mpesa):
            raise ValidationError("Enter a valid Mpesa Code")
        if LoanOrderInstallments.objects.filter(mpesa_code=mpesa).exists() or \
                OrderPayment.objects.filter(mpesa_code=mpesa).exists() or \
                LoanRepaymentTransaction.objects.filter(mpesa_code=mpesa).exists() or \
                SavingTransaction.objects.filter(mpesa_code=mpesa).exists():
            raise ValidationError("Mpesa Code already used.")
        return mpesa
