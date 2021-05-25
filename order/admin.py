from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Замовлення"""
    list_display = ("id", "first_name", "last_name")
    list_display_links = ("id", "first_name")
    search_fields = ("first_name",)
