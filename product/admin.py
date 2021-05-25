from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категорії"""
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    prepopulated_fields = {"slug": ("name",)}


class ShortImgProductInlines(admin.TabularInline):
    model = ShortImgProduct
    extra = 0


class SpecInlines(admin.TabularInline):
    model = Spec
    fk_name = "product"
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [SpecInlines, ShortImgProductInlines]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Планшети"""
    list_display = ("id", "user")
    list_display_links = ("id", "user")
    readonly_fields = ('order',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Планшети"""
    list_display = ("id",)
    list_display_links = ("id",)
    readonly_fields = ('in_order',)


admin.site.register(CartProduct)
admin.site.register(Review)
