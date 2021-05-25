from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, RequestFactory
from ..views import *
from ..models import *


User = get_user_model()


class TestProductView(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username="user1", password="1111")
        self.category = Category.objects.create(name='Pc', slug='pc')
        self.product = Product.objects.create(
            title='product',
            slug='product',
            category=self.category,
            quantity_in_stock=20,
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            price=Decimal("1000.00")
        )
        self.customer = Customer.objects.create(user=self.user)

        self.cart = Cart.objects.create(customer=self.customer)
        self.cart_product = CartProduct.objects.create(
            user=self.customer,
            cart=self.cart,
            product=self.product
        )

        self.client = Client()
        self.factory = RequestFactory()

    def test_home_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_category(self):
        response = self.client.get(f'/category/{self.category.slug}')
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_view(self):
        self.cart.products.add(self.cart_product)
        request = self.factory.get('')
        request.user = self.user
        response = AddToCartView.as_view()(request, product_model=f'{self.category.slug}', slug=f'{self.product.slug}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')
        self.assertIn(self.cart_product, self.cart.products.all())
        self.assertTrue(self.cart.products.count(), 1)

    def test_delete_to_cart_view(self):
        self.cart.products.remove(self.cart_product)
        request = self.factory.get('')
        request.user = self.user
        response = DeleteFromCartView.as_view()(request, product_model=f'{self.category.slug}',
                                                slug=f'{self.product.slug}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')
        self.assertNotIn(self.cart_product, self.cart.products.all())

    def test_detail_product_page(self):
        request = self.factory.get('', {'count': 1})
        request.user = self.user
        response = ProductDetailView.as_view()(request, product_model=f'{self.category.slug}',
                                               slug=f'{self.product.slug}')
        self.assertEqual(response.status_code, 200)

    def test_cart_page(self):
        request = self.factory.get('')
        request.user = self.user
        response = CartView.as_view()(request, product_model=f'{self.category.slug}',
                                               slug=f'{self.product.slug}')
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        res = self.client.get('/logout')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, '/accounts/login/')

    def test_add_review_to_product(self):
        res = self.client.post(f'/review/{self.category.slug}/{self.product.slug}', {'review': 'text',
                                                                                     'user': self.user,
                                                                                     'product': self.product
                                                                                     })
        self.assertEqual(res.status_code, 302)

