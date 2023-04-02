import re

from braces.forms import UserKwargModelFormMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm, ModelChoiceField

from loan.models import LoanApplication, Saving, SavingTransaction, LoanRepaymentTransaction, LoanRepayment, \
    SavingsWithdrawal
from stock.models import LoanOrderInstallments, OrderPayment

User: AbstractUser = get_user_model()


class SavingModelForm(ModelForm):
    user = ModelChoiceField(queryset=User.objects.filter(Q(type="CM") | Q(type="RD")).exclude(is_staff=True),
                            empty_label="Select User")

    class Meta:
        model = Saving
        fields = ['user', 'amount']


class LoanApplicationModelForm(UserKwargModelFormMixin, ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['amount', 'purpose', 'type']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if LoanApplication.objects.filter(user=self.user, status="PG").exists():
            raise ValidationError("Sorry you have another loan application pending")
        if Saving.objects.filter(user=self.user).exists():
            saving = Saving.objects.filter(user=self.user).first()
            if amount > saving.loan_limit():
                raise ValidationError(f"sorry your loan limit is {saving.loan_limit()}")
        else:
            raise ValidationError("sorry your loan limit is 0")
        return amount


class SavingTransactionModelForm(ModelForm):
    class Meta:
        model = SavingTransaction
        fields = ['amount', 'mpesa_code']

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


class LoanRepaymentTransactionModelForm(UserKwargModelFormMixin, ModelForm):
    repayment = ModelChoiceField(queryset=LoanRepayment.objects.filter(paid=False),
                                 empty_label="Select Loan Installment")

    def __init__(self, *args, **kwargs):
        super(LoanRepaymentTransactionModelForm, self).__init__(*args, **kwargs)
        self.fields["repayment"].queryset = self.fields["repayment"].queryset.filter(loan__user=self.user)

    class Meta:
        model = LoanRepaymentTransaction
        fields = ['repayment', 'mpesa_code']

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


class SavingsWithdrawalModelForm(UserKwargModelFormMixin, ModelForm):
    class Meta:
        model = SavingsWithdrawal
        fields = ['amount']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        saving = Saving.objects.filter(user=self.user).first()
        if amount.amount < 1:
            raise ValidationError("Amount has to be greater than 0")
        if amount > saving.amount:
            raise ValidationError(f"Sorry you remaining balance is {saving.amount}")
        return amount

