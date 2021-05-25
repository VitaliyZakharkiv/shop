from django.test import TestCase
from django.urls import resolve, reverse
from ..views import *


class TestProfileUrl(TestCase):
    def setUp(self) -> None:
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.profile_url = reverse('profile')

    def test_login_url(self):
        self.assertEqual(resolve(self.login_url).func.view_class, UserLogin)

    def test_register_url(self):
        self.assertEqual(resolve(self.register_url).func.view_class, RegisterLogin)

    def test_profile_url(self):
        self.assertEqual(resolve(self.profile_url).func.view_class, ProfileView)
