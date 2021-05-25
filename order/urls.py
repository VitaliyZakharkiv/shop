from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('make-order/', MakeOrderView.as_view(), name="order")
]
