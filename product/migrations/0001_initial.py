# Generated by Django 3.2 on 2021-04-16 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name="Ім'я")),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Категорія',
                'verbose_name_plural': 'Категорії',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255, verbose_name="Ім'я")),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='images_product/', verbose_name='Фото')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Ціна')),
                ('brand', models.CharField(max_length=255, verbose_name='Бренд')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category', verbose_name='Категорії')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукти',
            },
        ),
        migrations.CreateModel(
            name='ShortImgProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='product/', verbose_name='Фото')),
                ('mdl', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'verbose_name': 'Кадри ноутбука',
                'verbose_name_plural': 'Кадри ноутбуків',
            },
        ),
        migrations.CreateModel(
            name='Spec',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.product')),
                ('key', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prod', to='product.product')),
            ],
            options={
                'verbose_name': 'Специфікація',
                'verbose_name_plural': 'Специфікації',
            },
            bases=('product.product',),
        ),
    ]
