from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class LoginEmailBackend(ModelBackend):
    """authorization using email"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.filter(email=username).first()
        try:
            if user.check_password(password) and user is not None:
                return user
        except AttributeError:
            pass
