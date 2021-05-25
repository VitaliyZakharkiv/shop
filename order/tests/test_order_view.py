from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from ..views import *

User = get_user_model()


class TestProductView(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='Vitalik', password='1111')
        self.f = RequestFactory()

    def test_make_order_view(self):
        request = self.f.post('/make-order/', {'first_name': 'Vitalik',
                                               'last_name': 'Zakharkiv',
                                               'phone': '13548946',
                                               'address': 'address',
                                               'type_order': 'Самовивоз',
                                               'order_date': ' datetime.date(2021, 5, 20)'})
        request.user = self.user
        res = MakeOrderView.as_view()(request)
        self.assertEqual(res.status_code, 302)

    def test_checkout_view(self):
        request = self.f.get('/checkout/')
        request.user = self.user
        res = CheckoutView.as_view()(request)
        self.assertEqual(res.status_code, 200)
