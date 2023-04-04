from django.db import models
from decimal import Decimal
from django.conf import settings
from accounts.models import User
from core.utils import TimeStampModel
from stock.models import Product
from moneyed import Money
from djmoney.models.fields import MoneyField

        
class SupplyTender(TimeStampModel):
    date = models.DateTimeField(auto_now_add=True, null=True)
    delivery_date = models.DateField(null= True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='needs_supply', null=True, verbose_name='supplier')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='KES', verbose_name='Design Price', null=True)
    quantity = models.IntegerField()    
    status = (
        ('Pending','Pending'),
        ('Accepted','Accepted'),
        ('Approved', 'Approved'),
        ('Supplied', 'Supplied'),
        ('Rejected','Rejected'),
        ('Confirmed','Confirmed'),
        ('Paid','Paid'),
        ('Complete','Complete'),
    )
    tender_status = models.CharField(max_length=50, choices=status, default='Pending')

    class Meta:
        verbose_name_plural = 'Supply Tenders'
    
    def __str__(self):
        return f"{self.quantity} units of {self.product.name}"

    def total(self):
        return self.price * self.quantity



    def __str__(self):
        return '{} units of {}'.format(self.quantity, self.product.name)





