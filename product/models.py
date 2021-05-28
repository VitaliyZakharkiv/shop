import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from order.models import Order


User = get_user_model()


class Category(models.Model):
    """Модель категорій"""
    name = models.CharField(max_length=255, verbose_name="Ім'я")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Product(models.Model):
    """Модель продуктів"""
    category = models.ForeignKey(Category, verbose_name="Категорії", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True, verbose_name="Ім'я")
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='images_product/', verbose_name="Фото", null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=1, verbose_name="Ціна")
    quantity_in_stock = models.PositiveIntegerField(verbose_name="Кількість на складі", default=0)
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"

    def checking_availability_in_stock(self):
        return self.quantity_in_stock > 0

    def __str__(self):
        return f'Продукт {self.title} Категорії {self.category}'

    def get_brand_product(self):
        return Product.objects.filter(
            spec__key='Бренд', slug=self.slug).values('spec__value').first()['spec__value']

    def get_absolute_url(self):
        return reverse('detail_product', kwargs={'category_id': self.category.slug, 'slug': self.slug})

    def new_product(self):
        return self.date >= (timezone.now() - datetime.timedelta(days=1))


class Spec(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Специфікація'
        verbose_name_plural = 'Специфікації'


class ShortImgProduct(models.Model):
    mdl = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    img = models.ImageField(upload_to='product/', verbose_name="Фото")

    def __str__(self):
        return self.mdl.title

    class Meta:
        verbose_name = 'Кадри ноутбука'
        verbose_name_plural = 'Кадри ноутбуків'


class CartProduct(models.Model):
    """Карточка товара"""
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name="Покупець")
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name="Корзина", related_name="related_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    count = models.PositiveIntegerField(default=1)
    all_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name="Вся сума")

    def __str__(self):
        return f"{self.id}"

    def save(self, *args, **kwargs):
        self.all_price = self.count * self.product.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Карта Продукта"
        verbose_name_plural = "Карта Продуктів"


class Customer(models.Model):
    """Покупець"""
    user = models.ForeignKey(User, verbose_name="Покупець", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес")
    order = models.ManyToManyField('order.Order', related_name='orders_customer', verbose_name="Замовлення")

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = "Покупець"
        verbose_name_plural = "Покупці"


class Cart(models.Model):
    """Корзина"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, verbose_name="Покупець")
    products = models.ManyToManyField(CartProduct, blank=True, related_name="related_cart")
    all_product = models.PositiveIntegerField(default=0, null=True, blank=True)
    all_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, verbose_name="Вся сума")
    discount = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name="Сума із знижкою")
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer} - {self.products}"

    def count_product_in_cart(self):
        c = self.products.aggregate(models.Sum('count'))
        if c['count__sum'] is None:
            return {'count__sum': 0}
        return c

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"


class Review(models.Model):
    """Відгуки"""
    review = models.TextField(verbose_name="Відгук")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

