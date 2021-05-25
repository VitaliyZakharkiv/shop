from django.db import models
from django.utils import timezone


class Order(models.Model):
    """Замовлення"""
    STATUS = (
        ('NEW', 'Новий'),
        ('PROGRESS', 'В обробці'),
        ('READY', 'Готовий'),
        ('COMPLETED', 'Виконаний')
    )

    TYPE_ORDER = (
        ('SELF', 'Самовивоз'),
        ('DELIVERY', 'Доставка')
    )

    customer = models.ForeignKey(
                                'product.Customer',
                                on_delete=models.CASCADE,
                                related_name='order_customer',
                                verbose_name='Покупець'
                                )
    first_name = models.CharField(verbose_name='Імя', max_length=255)
    last_name = models.CharField(verbose_name='Прізвище', max_length=255)
    phone = models.CharField(verbose_name='Номер', max_length=255)
    address = models.CharField(verbose_name='Адрес', blank=True, null=True, max_length=255)
    status = models.CharField(verbose_name='Статус', max_length=255, choices=STATUS, default=STATUS[0][1])
    type_order = models.CharField(verbose_name='Тип доставки', max_length=255, choices=TYPE_ORDER, default=TYPE_ORDER[0][1])
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата замовлення')
    order_date = models.DateField(verbose_name='Дата на виконання', default=timezone.now())
    cart = models.ForeignKey('product.Cart', on_delete=models.CASCADE, verbose_name='Корзина', blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Замолення'
        verbose_name_plural = 'Замолення'
