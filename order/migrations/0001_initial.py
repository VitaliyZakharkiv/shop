# Generated by Django 3.2 on 2021-04-16 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Імя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Прізвище')),
                ('phone', models.CharField(max_length=255, verbose_name='Номер')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес')),
                ('status', models.CharField(choices=[('NEW', 'Новий'), ('PROGRESS', 'В обробці'), ('READY', 'Готовий'), ('COMPLETED', 'Виконаний')], default='Новий', max_length=255, verbose_name='Статус')),
                ('type_order', models.CharField(choices=[('SELF', 'Самовивоз'), ('DELIVERY', 'Доставка')], default='Самовивоз', max_length=255, verbose_name='Тип доставки')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата замовлення')),
                ('order_date', models.DateField(auto_now_add=True, verbose_name='Дата на виконання')),
            ],
            options={
                'verbose_name': 'Замолення',
                'verbose_name_plural': 'Замолення',
            },
        ),
    ]
