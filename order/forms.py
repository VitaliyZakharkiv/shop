from datetime import date
from django import forms
from django.core.exceptions import ValidationError


from .models import Order


class OrderForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Введіть ім'я"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введіть прізвище'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введіть телефон', 'type': 'tel'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введіть адрес'}))
    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone', 'address', 'type_order', 'order_date')

    def clean_order_date(self):
        date_order = self.cleaned_data['order_date']
        data_today = date.today()
        if data_today > date_order:
            raise ValidationError("Ви не можете це зробити")

        return date_order
