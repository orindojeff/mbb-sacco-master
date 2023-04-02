from braces.forms import UserKwargModelFormMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm, ModelChoiceField

from delivery.models import Location, PickUpStation, UserPickUpStation, OrderDelivery, LoanOrderDelivery

User: AbstractUser = get_user_model()


class LocationModelForm(ModelForm):
    class Meta:
        model = Location
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name.lower()


class PickUpStationModelForm(ModelForm):
    location = ModelChoiceField(queryset=Location.objects.all(), empty_label="Select Location")

    class Meta:
        model = PickUpStation
        fields = ['name', 'location']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name.lower()


class AdminUserPickUpStationModelForm(ModelForm):
    user = ModelChoiceField(queryset=User.objects.filter(Q(type="CM") | Q(type="RD")).exclude(is_staff=True),
                            empty_label="Select User")
    station = ModelChoiceField(queryset=PickUpStation.objects.all(), empty_label="Select pickup station")

    class Meta:
        model = UserPickUpStation
        fields = ['user', 'station']


class UserPickUpStationModelForm(UserKwargModelFormMixin, ModelForm):
    station = ModelChoiceField(queryset=PickUpStation.objects.all(), empty_label="Select pickup station")

    class Meta:
        model = UserPickUpStation
        fields = ['station']

    def clean_station(self):
        station = self.cleaned_data.get("station")
        if UserPickUpStation.objects.filter(user=self.user, station=station).exists():
            raise ValidationError("pickup station already selected")
        return station


class OrderDeliveryModelForm(ModelForm):
    class Meta:
        model = OrderDelivery
        fields = ["driver"]


class LoanOrderDeliveryModelForm(ModelForm):
    class Meta:
        model = LoanOrderDelivery
        fields = ["driver"]
