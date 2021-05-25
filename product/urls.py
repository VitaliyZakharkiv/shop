from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('logout', UserLogout.as_view(), name='logout'),
    path('category/<slug:slug>', CategoryDetailView.as_view(), name="category"),
    path('cart/', CartView.as_view(), name="cart"),
    path('category/<slug:category_id>/<slug:slug>', ProductDetailView.as_view(), name="detail_product"),
    path('add/<slug:product_model>/<slug:slug>', AddToCartView.as_view(), name="add-to-cart"),
    path('delete/<slug:product_model>/<slug:slug>', DeleteFromCartView.as_view(), name="delete-from-cart"),
    path('change/<slug:product_model>/<slug:slug>', ChangeCountView.as_view(), name="change-count"),
    path('review/<slug:product_model>/<slug:slug>', AddReviewView.as_view(), name="add-review")
]
