from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _
from djmoney.money import Money
from decimal import Decimal

from core.utils import TimeStampModel

User: AbstractUser = get_user_model()


class Saving(TimeStampModel):
    class Status(models.TextChoices):
        PENDING = 'PG', _('Pending')
        APPROVED = 'AP', _('Approved')
        DECLINED = 'DC', _('Declined')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="savings")
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES', null=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING)


    def loan_limit(self):
        limit = 0
        if self.amount:
            limit = self.amount.amount * 2
        return Money(limit, "KES")

    def get_status_display(self):
        return self.Status(self.status).label


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

class LoanAccount(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES', default=0)

class Account(TimeStampModel):
    name = models.CharField(max_length=255, null=True)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')


class LoanRepayment(TimeStampModel):
    loan = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    paid = models.BooleanField(default=False)
    min_repayment = MoneyField(max_digits=14, decimal_places=2, default_currency='KES', null=True, blank=True)

    def __str__(self):
        return str(self.amount)

    def save(self, *args, **kwargs):
        if not self.min_repayment:
            self.min_repayment = self.calculate_min_repayment()
        super().save(*args, **kwargs)

    def calculate_min_repayment(self):
        # Calculate monthly installment based on loan type
        if self.loan.type == LoanApplication.LoanType.MONTHLY:
            installment = self.loan.amount * Decimal('1.05') / 12
        elif self.loan.type == LoanApplication.LoanType.THREE_MONTHS:
            installment = self.loan.amount * Decimal('1.10') / 3
        elif self.loan.type == LoanApplication.LoanType.HALF_YEAR:
            installment = self.loan.amount * Decimal('1.15') / 6
        else:
            installment = self.loan.amount * Decimal('1.20') / 12
        # Set minimum repayment to monthly installment
        return installment





class LoanRepaymentTransaction(TimeStampModel):
    repayment = models.ForeignKey(LoanRepayment, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    mpesa_code = models.CharField(max_length=10)
    confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update LoanRepayment's min_repayment field with the calculated minimum repayment
        self.repayment.min_repayment = self.repayment.calculate_min_repayment()
        self.repayment.save()




class SavingsWithdrawal(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="savings_withdrawal")
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')

