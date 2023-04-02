from django.db.models.signals import post_save
from django.dispatch import receiver
from djmoney.money import Money

from loan.models import LoanApplication, LoanRepayment, SavingTransaction, SavingsWithdrawal, Saving


@receiver(post_save, sender=LoanApplication, dispatch_uid="creating_loan_repayment")
def creating_loan_repayment(sender, instance, created, **kwargs):
    if created:
        if instance.type == "M":
            LoanRepayment.objects.create(loan=instance, amount=instance.amount)
        elif instance.type == "TM":
            amount = instance.amount.amount
            monthly_payment_amount = amount / 3
            loan_repayment_objs = [LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                                   LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                                   LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES"))]
            LoanRepayment.objects.bulk_create(loan_repayment_objs)
        elif instance.type == "HY":
            amount = instance.amount.amount
            monthly_payment_amount = amount / 6
            loan_repayment_objs = [
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
            ]
            LoanRepayment.objects.bulk_create(loan_repayment_objs)
        elif instance.type == "Y":
            amount = instance.amount.amount
            monthly_payment_amount = amount / 12
            loan_repayment_objs = [
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
                LoanRepayment(loan=instance, amount=Money(monthly_payment_amount, "KES")),
            ]
            LoanRepayment.objects.bulk_create(loan_repayment_objs)
    else:
        if instance.status == "AP":
            saving = Saving.objects.filter(user=instance.user).first()
            saving.amount += instance.amount
            saving.save()


@receiver(post_save, sender=SavingTransaction, dispatch_uid="update_savings")
def update_savings(sender, instance, created, **kwargs):
    if created:
        saving = instance.saving
        total_saving = instance.amount.amount
        if saving.amount:
            current_saving_amount = saving.amount.amount
            total_saving += current_saving_amount
        saving.amount = Money(total_saving, "KES")
        saving.save()


@receiver(post_save, sender=SavingsWithdrawal, dispatch_uid="update_savings_after_withdrawal")
def update_savings_after_withdrawal(sender, instance, created, **kwargs):
    if created:
        saving = Saving.objects.filter(user=instance.user).first()
        withdrawn_amount = instance.amount.amount
        current_saving_amount = saving.amount.amount
        current_saving_amount -= withdrawn_amount
        saving.amount = Money(current_saving_amount, "KES")
        saving.save()
