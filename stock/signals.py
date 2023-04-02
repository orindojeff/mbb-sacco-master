from django.db.models.signals import post_save
from django.dispatch import receiver

from stock.models import Product, ProductLoan


@receiver(post_save, sender=Product, dispatch_uid="creating_product_loans")
def creating_product_loans(sender, instance, created, **kwargs):
    if created:
        product_loan_objs = [ProductLoan(product=instance, duration='OY'), ProductLoan(product=instance, duration='TY'),
                             ProductLoan(product=instance, duration='THY')]
        ProductLoan.objects.bulk_create(product_loan_objs)
