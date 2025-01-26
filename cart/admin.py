from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Cart, CartItem

# Register your models here.

@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    date_hierarchy = 'created_at'

@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity', 'get_total_price']
    list_filter = ['cart__created_at']
    search_fields = ['cart__user__username', 'product__name']
    raw_id_fields = ['cart', 'product']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price
    get_total_price.short_description = 'Total Price'
