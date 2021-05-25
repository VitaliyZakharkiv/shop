from django import forms
from .models import Order


class OrderForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Введіть ім'я"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введіть прізвище'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введіть телефон'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введіть адрес'}))
    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone', 'address', 'type_order', 'order_date')
