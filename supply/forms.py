from django import forms
from accounts.models import User
from django import forms
from .models import  SupplyTender
from django import forms
from django.contrib.auth import get_user_model
from .models import SupplyTender



from django.forms.widgets import DateInput

class SupplyTenderForm(forms.ModelForm):
    
    class Meta:
        model = SupplyTender
        fields = ['product', 'quantity', 'delivery_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['delivery_date'].widget = DateInput(attrs={'type': 'date', 'class': 'form-control'})


