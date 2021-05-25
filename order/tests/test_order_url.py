from django.test import TestCase
from django.urls import resolve, reverse
from ..views import *


class TestOrderUrl(TestCase):
    def setUp(self) -> None:
        self.checkout_url = reverse('checkout')
        self.make_order_url = reverse('order')

    def test_checkout_url(self):
        self.assertEqual(resolve(self.checkout_url).func.view_class, CheckoutView)

    def test_make_order_url(self):
        self.assertEqual(resolve(self.make_order_url).func.view_class, MakeOrderView)
