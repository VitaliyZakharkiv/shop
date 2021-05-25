from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from .models import Category, Cart, Customer, CartProduct
from django.db import models


class CommonMixin(SingleObjectMixin):
    """Mixin for showing category"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CartMixin(View):
    """Mixin for basket"""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            # customer = Customer.objects.filter(user=request.user).first()
            # cart = Cart.objects.filter(customer=customer, in_order=False).first()
            # if not customer:
            #     customer = Customer.objects.create(
            #         user=request.user
            #     )

            cart = Cart.objects.filter(customer__user=request.user, in_order=False).first()

            if not cart:
                cart = Cart.objects.create(
                    customer__user=request.user
                )
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)


def save_cart(cart):
    """An analogue of the `save ()` method"""
    cart_product = cart.products.aggregate(models.Sum('all_price'), models.Sum('count'))
    count = cart_product['count__sum']
    if cart_product.get('all_price__sum'):
        if count >= 3 and count <= 5:
            cart.discount = cart_product['all_price__sum'] - (cart_product['all_price__sum'] * 5) / 100
            cart.all_price = 0
        elif count > 5:
            cart.discount = cart_product['all_price__sum'] - (cart_product['all_price__sum'] * 10) / 100
            cart.all_price = 0
        else:
            cart.all_price = cart_product['all_price__sum']
            cart.discount = 0
    else:
        cart.discount = 0
        cart.all_price = 0

    cart.all_product = cart_product['count__sum']
    cart.save()
