from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock_quantity", "is_active")
    # prepopulated_fields = {"slug": ("name",)}


# admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
