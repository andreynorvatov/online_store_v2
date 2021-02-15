from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    email = forms.EmailInput()

    class Meta:
        model = Order
        fields = ('name', 'phone', 'email')
