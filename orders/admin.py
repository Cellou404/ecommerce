from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'payment_status', 'paid']
    list_filter = ['payment_status', 'paid', 'created_at', 'updated_at']
    list_editable = ['payment_status', 'paid']
    inlines = [OrderItemInline]
    search_fields = ['first_name', 'last_name', 'email']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']
    list_filter = ['order__payment_status', 'order__paid']
    search_fields = ['order__id', 'product__name']
    raw_id_fields = ['order', 'product']
