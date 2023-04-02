from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.utils import TimeStampModel
from stock.models import Order, LoanOrder

User: AbstractUser = get_user_model()


class Location(TimeStampModel):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class PickUpStation(TimeStampModel):
    name = models.CharField(max_length=250)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'location']

    def __str__(self):
        return f"{self.location.name} - {self.name}"


class UserPickUpStation(TimeStampModel):
    station = models.ForeignKey(PickUpStation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pickup_stations")
    selected = models.BooleanField(default=False)

    class Meta:
        unique_together = ['station', 'user']

    def __str__(self):
        return f"{self.station} [{self.user}]"


class Delivery(TimeStampModel):
    class Status(models.TextChoices):
        PENDING = 'PG', _('Pending')
        IN_TRANSIT = 'IT', _('In Transit')
        ARRIVED = 'AR', _('Arrived')
    station = models.ForeignKey(UserPickUpStation, on_delete=models.CASCADE)
    picked = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING)

    class Meta:
        abstract = True


class OrderDelivery(Delivery):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="driver_orders", null=True)


class LoanOrderDelivery(Delivery):
    order = models.ForeignKey(LoanOrder, on_delete=models.CASCADE)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="driver_loan_orders", null=True)
