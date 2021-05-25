from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView
from product.forms import ReviewForm
from product.mixins import CartMixin, save_cart, CommonMixin
from product.models import Category, Product, CartProduct, Review, Cart


class HomeView(CartMixin, View):
    """Home page"""
    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        product = Product.objects.all().order_by('-id')[:4].select_related('category')

        context = {
            'product': product,
            'categories': category,
            'cart': self.cart
        }
        return render(request, 'product/base.html', context)


class CategoryDetailView(CommonMixin, CartMixin, DetailView):
    """Category product"""
    model = Category
    template_name = 'product/detail_page.html'
    context_object_name = 'category'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.category_slug = self.kwargs.get('slug')

        context['specifications'] = self.set_list(Product.objects.filter(
            category__slug=self.category_slug).values('spec__key', 'spec__value'))

        context['cart'] = self.cart
        context['q'] = self.get_filter_date()
        context['name'] = self.get_auto_name()

        if self.find():
            context['find'] = self.page_pagination(self.find())
        elif self.request.GET.getlist('specification'):
            context['filter_product'] = self.page_pagination(
                self.set_list(Product.objects.select_related('category').filter(
                    spec__value__in=self.request.GET.getlist('specification'), category__slug=self.category_slug)))
        else:
            context['products'] = self.page_pagination(Product.objects.select_related('category').filter(
                category__slug=self.category_slug)[::-1])

        return context

    def find(self):
        """Search"""
        q = self.request.GET.get('q')
        if q:
            return Product.objects.select_related('category').filter(title__istartswith=q,
                                                                     category__slug=self.category_slug)

    def get_auto_name(self):
        """Автоматичні імена, для пошуку"""
        qs = Product.objects.filter(category__slug=self.category_slug).values('title')
        name = []
        for i in qs:
            name.append(i['title'])
        return name

    def set_list(self, array):
        """Unique fields filter"""
        d = []
        for i in list(array):
            if i not in d:
                d.append(i)
            else:
                continue
        return d

    def get_filter_date(self):
        """Get link"""
        p = self.request.GET
        s = []
        for i in p:
            if i != 'page':
                s.append(''.join([f'{i}={j}&' for j in self.request.GET.getlist(i)]))
            else:
                break
        link = ''.join(s)
        return link

    def page_pagination(self, qs):
        """Pagination"""
        element = Paginator(qs, 9)
        page_num = self.request.GET.get('page', 1)

        try:
            page = element.page(page_num)
        except EmptyPage:
            page = element.page(1)
        return page


class ProductDetailView(CommonMixin, CartMixin, DetailView):
    """Separate product"""
    model = Product
    queryset = Product.objects.select_related('category')
    template_name = 'product/detail_product.html'
    context_object_name = "product"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        context['form'] = ReviewForm()
        context['review'] = Review.objects.filter(product__slug=self.kwargs.get('slug')).select_related('user')
        return context


class CartView(LoginRequiredMixin, CartMixin, View):
    """Basket"""
    login_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart,
            'categories': Category.objects.all()
        }
        return render(request, 'product/cart.html', context)


class AddToCartView(LoginRequiredMixin, CartMixin, View):
    """Add product in basket"""
    login_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        slug_product = kwargs.get('slug')
        product = Product.objects.filter(slug=slug_product).first()
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.customer, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        save_cart(self.cart)
        return redirect('cart')


class DeleteFromCartView(CartMixin, View):
    """Delete product basket"""
    def get(self, request, *args, **kwargs):
        slug_product = kwargs.get('slug')
        product = Product.objects.filter(slug=slug_product).first()
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.customer, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        save_cart(self.cart)
        return redirect('cart')


class ChangeCountView(CartMixin, View):
    """Change quantity"""
    def post(self, request, *args, **kwargs):
        slug_product = kwargs.get('slug')
        product = Product.objects.filter(slug=slug_product).first()
        cart_product = CartProduct.objects.get(
            user=self.cart.customer, cart=self.cart, product=product
        )

        count = int(request.POST.get('count'))
        cart_product.count = count
        cart_product.save()
        save_cart(self.cart)
        return redirect('cart')


class UserLogout(LogoutView):
    """клас для кнопки виходу з профіля"""
    next_page = reverse_lazy('login')


# class AddReviewView(View):
#     """Добавлення відгуку"""
#     def post(self, request, *args, **kwargs):
#         form = ReviewForm(request.POST)
#         slug_product = kwargs.get('slug')
#         product = Product.objects.filter(slug=slug_product).first()
#         if form.is_valid():
#             form = form.save(commit=False)
#             form.review = request.POST.get('review')
#             form.user = request.user
#             form.product = product
#             form.save()
#
#         return redirect(product.get_absolute_url())


class AddReviewView(LoginRequiredMixin, CreateView):
    """Add review"""
    model = Review
    form_class = ReviewForm
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.review = self.request.POST.get('review')
        form.instance.user = self.request.user
        form.instance.product = Product.objects.filter(slug=self.kwargs.get('slug')).first()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail_product', kwargs={'category_id': self.kwargs.get('category_id'),
                                                      'slug': self.kwargs.get('slug')})
