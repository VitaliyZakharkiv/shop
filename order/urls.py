from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('receipt/', render_pdf_view, name="receipt"),
    path('make-order/', MakeOrderView.as_view(), name="order"),

    path('print/', PrintReceiptView.as_view(), name="print")
]
