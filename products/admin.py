from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product, ProductVariation

# Register your models here.

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug', 'get_products_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def get_products_count(self, obj):
        return obj.products.count()
    get_products_count.short_description = 'Products Count'

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    date_hierarchy = 'created'
    ordering = ['name']
    readonly_fields = ['created', 'updated']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'available')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProductVariation)
class ProductVariationAdmin(ModelAdmin):
    list_display = ['product', 'color', 'size', 'stock_quantity', 'price_override']
    list_filter = ['product', 'color', 'size']
    search_fields = ['product__name', 'color', 'size']
