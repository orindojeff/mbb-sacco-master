from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from core.utils import TimeStampModel


class User(AbstractUser):
    class UserTypes(models.TextChoices):
        DRIVER = 'DR', _('Driver')
        FINANCE_MANAGER = 'FM', _('Finance')
        SALES_MANAGER = 'SM', _('Sales')
        RIDER = 'RD', _('Rider')
        CUSTOMER = 'CM', _('Customer')
        SUPPLIER = 'SP', _('Supplier')

    type = models.CharField(max_length=2, choices=UserTypes.choices, default=UserTypes.CUSTOMER)
    name = models.CharField(max_length=250)
    is_verified = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def has_selected_pickup_station(self):
        has_selected_station = False
        for station in self.pickup_stations.all():
            if station.selected:
                has_selected_station = True
        return has_selected_station


class Profile(TimeStampModel):
    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='profiles/%Y/%m/', default="profiles/default.png")
    gender = models.CharField(max_length=2, choices=Gender.choices, default=Gender.FEMALE)
    phone_number = PhoneNumberField(blank=True, null=True)
    is_verified = models.BooleanField(_("Verified"), default=False, help_text="Means phone number is verified")


class FAQ(TimeStampModel):
    class FAQTypes(models.TextChoices):
        DRIVER = 'DR', _('Driver')
        FINANCE_MANAGER = 'FM', _('Finance Manger')
        SALES_MANAGER = 'SM', _('Sales Manager')
        RIDER = 'RD', _('Rider')
        CUSTOMER = 'CM', _('Customer')
        ALL = 'ALL', _('Driver, Customer, Rider, Sales Manager, Finance Manger')

    name = models.CharField(max_length=250)
    content = RichTextUploadingField(_('content'))
    type = models.CharField(_('FAQ Category'), max_length=3, choices=FAQTypes.choices, default=FAQTypes.ALL)


class DialogsModel(TimeStampModel):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+", db_index=True)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+", db_index=True)

    class Meta:
        unique_together = (('customer', 'staff'), ('customer', 'staff'))
        verbose_name = _("Dialog")
        verbose_name_plural = _("Dialogs")

    def __str__(self):
        return _("Dialog between ") + f"{self.customer.name}, {self.staff.name}"


class Feedback(TimeStampModel):
    class DialogType(models.TextChoices):
        CUSTOMER_VS_FINANCE_MANAGER = 'CST_FMR', _('Finance Manager')
        FINANCE_MANAGER_VS_CUSTOMER = 'FMR_CST', _('Customer / Rider')
        CUSTOMER_VS_SALES_MANAGER = 'CST_SMR', _('Sales Manager')
        SALES_MANAGER_VS_CUSTOMER = 'SMR_CST', _('Customer / Rider')

    dialog = models.ForeignKey(DialogsModel, on_delete=models.CASCADE, null=True, related_name='feedback')
    content = RichTextUploadingField(_('content'))
    type = models.CharField(
        _('Feedback type'), max_length=10, choices=DialogType.choices, default=DialogType.CUSTOMER_VS_FINANCE_MANAGER
    )

    def __str__(self):
        return str(self.dialog)

    def has_been_sent(self):
        was_sent = False
        if self.type == "CST_SMR" or self.type == "CST_FMR":
            was_sent = True
        return was_sent
