from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _
from djmoney.money import Money

from core.utils import TimeStampModel

User: AbstractUser = get_user_model()


class Saving(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="savings")
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES', null=True)

    def loan_limit(self):
        limit = 0
        if self.amount:
            limit = self.amount.amount * 2
        return Money(limit, "KES")


class SavingTransaction(TimeStampModel):
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE, related_name="transactions")
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    mpesa_code = models.CharField(max_length=10)
    confirmed = models.BooleanField(default=False)


class LoanApplication(TimeStampModel):
    class Status(models.TextChoices):
        PENDING = 'PG', _('Pending')
        APPROVED = 'AP', _('Approved')
        DECLINED = 'DC', _('Declined')

    class LoanType(models.TextChoices):
        MONTHLY = 'M', _('Monthly')
        THREE_MONTHS = 'TM', _('3 Months')
        HALF_YEAR = 'HY', _('6 Months')
        YEARLY = 'Y', _('12 Months')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    purpose = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING)
    type = models.CharField(max_length=2, choices=LoanType.choices, default=LoanType.MONTHLY)


class LoanRepayment(TimeStampModel):
    loan = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.amount)


class LoanRepaymentTransaction(TimeStampModel):
    repayment = models.ForeignKey(LoanRepayment, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    mpesa_code = models.CharField(max_length=10)
    confirmed = models.BooleanField(default=False)


class SavingsWithdrawal(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="savings_withdrawal")
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')

