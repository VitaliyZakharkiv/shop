from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.db import transaction
from product.mixins import CartMixin
from product.models import Customer, Category
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
    """Замовлення"""
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.filter(user=request.user).first()
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.address = form.cleaned_data['address']
            order.type_order = form.cleaned_data['type_order']
            order.order_date = form.cleaned_data['order_date']
            order.save()
            self.cart.in_order = True
            self.cart.save()
            order.cart = self.cart
            order.save()
            customer.order.add(order)
            return redirect('/')
        return redirect('checkout')

