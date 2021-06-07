from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.db import transaction
from product.mixins import CartMixin
from product.models import Category
from .forms import OrderForm
from .models import Order


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
            return redirect('print')
        messages.error(self.request, 'Дата не може бути раніше сьогоднішньої')
        return redirect('checkout')

    def calc_quantity_in_stock(self, cart_products):
        for i in cart_products:
            i.product.quantity_in_stock -= i.count
            i.product.save()


def render_pdf_view(request):
    order = Order.objects.filter(customer__user=request.user).last()
    template_path = 'order/receipt.html'
    context = {'order': order}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response)
    print(pisa_status)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def print_receipt_or_not(request):
    return render(request, 'order/o.html')


class PrintReceiptView(CartMixin, View):
    """Print receipt"""
    def get(self, request, *args, **kwargs):
        data = {
            "categories": Category.objects.all(),
            "cart": self.cart
        }
        return render(request, 'order/o.html', data)
