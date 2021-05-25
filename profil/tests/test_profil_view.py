from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from ..views import *
from ..models import *
from ..forms import UserRegisterForm, AuthUserForm

User = get_user_model()


class TestProfileView(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username="user1", password="1111")
        self.date = {
            'username': 'testuser',
            'first_name': 'nametest',
            'last_name': 'test',
            'email': 'emailtest@gmail.com',
            'password1': 'tfe6f2af#3g',
            'password2': 'tfe6f2af#3g'
        }
        self.date2 = {
            'username': 'testuser',
            'first_name': 'nametest',
            'last_name': 'test',
            'email': 'emailtest@gmail.com',
            'password1': 'text',
            'password2': 'text'
        }
        self.login = {
            'username': self.date['username'],
            'password': self.date['password1']
        }
        self.login2 = {
            'username': self.date2['username'],
            'password': self.date2['password1']
        }
        self.factory = RequestFactory()
        self.client = Client()

    def test_profile_page(self):
        request = self.factory.get('')
        request.user = self.user
        res = ProfileView.as_view()(request)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(self.user.is_authenticated)

    def test_register_user(self):
        client = self.client.post(reverse('register'), self.date)
        self.assertEqual(client.status_code, 302)

    def test_register_correct_date(self):
        form = UserRegisterForm(self.date)
        self.assertTrue(form.is_valid())

    def test_register_incorrect_date(self):
        form = UserRegisterForm(data=self.date2)
        self.assertFalse(form.is_valid())

    def test_login_user(self):
        client = self.client.post(reverse('login'), self.login)
        self.assertEqual(client.status_code, 200)

    def test_incorrect_date(self):
        form = AuthUserForm(data=self.login2)
        self.assertFalse(form.is_valid())

