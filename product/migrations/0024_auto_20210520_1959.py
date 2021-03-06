# Generated by Django 3.2 on 2021-05-20 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_alter_product_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartproduct',
            options={'default_related_name': 'products', 'verbose_name': 'Карта Продукта', 'verbose_name_plural': 'Карта Продуктів'},
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.product'),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.customer', verbose_name='Покупець'),
        ),
    ]
