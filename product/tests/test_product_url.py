from django.test import TestCase
from django.urls import resolve, reverse
from ..views import *


class TestProductUrl(TestCase):
    def setUp(self) -> None:
        self.home_url = reverse('home')
        self.logout_url = reverse('logout')
        self.category_url = reverse('category', args=['phone'])
        self.cart_url = reverse('cart')
        self.detail_product_url = reverse('detail_product', args=['phone', 'samsung-s8'])
        self.add_product_in_basket_url = reverse('add-to-cart', args=['phone', 'samsung-s8'])
        self.delete_product_basket_url = reverse('delete-from-cart', args=['phone', 'samsung-s8'])
        self.change_quantity_product_url = reverse('change-count', args=['phone', 'samsung-s8'])
        self.add_review_url = reverse('add-review', args=['phone', 'samsung-s8'])

    def test_home_url(self):
        self.assertEqual(resolve(self.home_url).func.view_class, HomeView)

    def test_logout_url(self):
        self.assertEqual(resolve(self.logout_url).func.view_class, UserLogout)

    def test_category_url(self):
        self.assertEqual(resolve(self.category_url).func.view_class, CategoryDetailView)

    def test_cart_url(self):
        self.assertEqual(resolve(self.cart_url).func.view_class, CartView)

    def test_detail_product_url(self):
        self.assertEqual(resolve(self.detail_product_url).func.view_class, ProductDetailView)

    def test_actions_on_product_url(self):
        self.assertEqual(resolve(self.add_product_in_basket_url).func.view_class, AddToCartView)
        self.assertEqual(resolve(self.delete_product_basket_url).func.view_class, DeleteFromCartView)
        self.assertEqual(resolve(self.change_quantity_product_url).func.view_class, ChangeCountView)

    def test_add_review_url(self):
        self.assertEqual(resolve(self.add_review_url).func.view_class, AddReviewView)
