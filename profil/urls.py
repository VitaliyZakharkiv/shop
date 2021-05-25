from django.urls import path
from .views import *

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('register/', RegisterLogin.as_view(), name='register'),
    path('account/', ProfileView.as_view(), name='profile')
]
