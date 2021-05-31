from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.db import transaction
from product.mixins import CartMixin
from product.models import Category
from .forms import OrderForm


class CheckoutView(LoginRequiredMixin, CartMixin, View):
    """Показ форми замовлення"""
    login_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {
            'form': form,
            'cart': self.cart,
            'categories': Category.objects.all()
        }
        return render(request, 'order/checkout.html', context)


class MakeOrderView(CartMixin, View):
    """Замовлення*"""
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = self.customer
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.address = form.cleaned_data['address']
            order.type_order = form.cleaned_data['type_order']
            order.order_date = form.cleaned_data['order_date']
            order.save()
            self.cart.in_order = True
            self.cart.save()
            self.calc_quantity_in_stock(self.cart.products.all())
            order.cart = self.cart
            order.save()
            self.customer.order.add(order)
            return redirect('/')
        messages.error(self.request, 'Дата не може бути раніше сьогоднішньої')
        return redirect('checkout')

    def calc_quantity_in_stock(self, cart_products):
        for i in cart_products:
            i.product.quantity_in_stock -= i.count
            i.product.save()
