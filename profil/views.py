from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic.base import View
from django.views.generic import CreateView
from django.shortcuts import render
from django.urls import reverse_lazy
from order.models import Order
from product.mixins import CartMixin
from product.models import Category, Customer
from profil.forms import AuthUserForm, UserRegisterForm


class UserLogin(LoginView):
    """
    Клас для авторизації
    """
    template_name = 'profil/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('home')

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
        ins = form.save()
        auth = authenticate(username=username, first_name=first_name, last_name=last_name, password=password,
                            email=email)
        login(self.request, auth)
        ins.email = email
        ins.last_name = last_name
        ins.first_name = first_name
        ins.save()
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
        customer = Customer.objects.filter(user=request.user).first()
        order = Order.objects.filter(customer=customer).order_by('-create_date')
        context = {
            'orders': order,
            'cart': self.cart,
            'categories': Category.objects.all()
        }
        return render(request, 'profil/profil.html', context)
