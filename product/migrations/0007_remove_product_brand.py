# Generated by Django 3.2 on 2021-04-19 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
    ]
