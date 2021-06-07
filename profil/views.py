import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db.models import Sum, Count, Case, When, F, Value, CharField
from django.views.generic.base import View
from django.views.generic import CreateView
from django.shortcuts import render
from django.urls import reverse_lazy

# from .tasks import send_message_on_email
from .service import sending_welcome_message_on_email_user
from order.models import Order
from product.mixins import CartMixin
from product.models import Category, Product
from profil.forms import AuthUserForm, UserRegisterForm

"""
amount customer
amount buy product
amount order
amount new product
"""

class UserLogin(LoginView):
    """
    Клас для авторизації
    """
    template_name = 'profil/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Неправильно введені логін або пароль')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class RegisterLogin(CreateView):
    """
    Клас для реєстрації
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'profil/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        last_name = form.cleaned_data['last_name']
        first_name = form.cleaned_data['first_name']
        email = form.cleaned_data['email']
        auth = authenticate(username=username, first_name=first_name, last_name=last_name, password=password,
                            email=email)

        login(self.request, auth)

        sending_welcome_message_on_email_user(email)
        # send_message_on_email.delay(email)
        return form_valid

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProfileView(LoginRequiredMixin, CartMixin, View):
    """
    Профіль користувача
    """
    login_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        self.test()
        order = Order.objects.filter(customer=self.customer)\
            .exclude(cart__all_price=None).select_related('cart') \
            .prefetch_related('cart__products__related_cart',
                              'cart__products__product') \
            .order_by('-create_date')
        context = {
            'orders': order,
            'cart': self.cart,
            'categories': Category.objects.all()
        }
        return render(request, 'profil/profil.html', context)

    def test(self):
        today = datetime.date.today()
        new_customer = User.objects.filter(date_joined__month=today.month)
        number_all_product_by_category = Category.objects.annotate(Count('product')).values('name', 'product__count')
        number_of_orders_per_month = Order.objects.filter(order_date__month=today.month)

        # send_mail(
        #     'Статистика',
        #     f'Кількість нових покупців -> {new_customer.count()}\n'
        #     f'Кількість продуктів по категоріям:\n'
        #     f'\tТелефони -> {number_all_product_by_category[2]["product__count"]}\n'
        #     f'\tКомп`ютери -> {number_all_product_by_category[1]["product__count"]}\n'
        #     f'\tНоутбуки -> {number_all_product_by_category[0]["product__count"]}\n'
        #     f'\tПланшети -> {number_all_product_by_category[3]["product__count"]}\n'
        #     f'Кількість оформлених замовлень -> {number_of_orders_per_month.aggregate(Count("cart"))["cart__count"]}\n'
        #     f'Кількість проданих товарів за цей місяць-> '
        #     f'{number_of_orders_per_month.aggregate(Count("cart__products"))["cart__products__count"]}',
        #     'vzaharkiv28@gmail.com',
        #     ['vzaharkiv28@gmail.com'],
        #     fail_silently=False
        # )
