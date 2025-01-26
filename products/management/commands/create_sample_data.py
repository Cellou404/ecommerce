from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from products.models import Category, Product, ProductVariation
import os
import shutil

class Command(BaseCommand):
    help = 'Create sample categories and products'

    def handle(self, *args, **kwargs):
        # Create sample categories
        categories = [
            {
                'name': 'Electronics',
                'slug': 'electronics',
            },
            {
                'name': 'Clothing',
                'slug': 'clothing',
            },
            {
                'name': 'Books',
                'slug': 'books',
            },
            {
                'name': 'Home & Kitchen',
                'slug': 'home-kitchen',
            },
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                slug=cat_data['slug']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category "{category.name}"'))

        # Create sample products
        products = [
            {
                'name': 'Laptop Pro',
                'slug': 'laptop-pro',
                'category': 'electronics',
                'description': 'High-performance laptop with the latest technology.',
                'price': 1299.99,
                'variations': [
                    {'color': 'Silver', 'size': None, 'stock_quantity': 50},
                    {'color': 'Space Gray', 'size': None, 'stock_quantity': 30}
                ]
            },
            {
                'name': 'Wireless Headphones',
                'slug': 'wireless-headphones',
                'category': 'electronics',
                'description': 'Premium wireless headphones with noise cancellation.',
                'price': 199.99,
                'variations': [
                    {'color': 'Black', 'size': None, 'stock_quantity': 100},
                    {'color': 'White', 'size': None, 'stock_quantity': 75}
                ]
            },
            {
                'name': 'Cotton T-Shirt',
                'slug': 'cotton-t-shirt',
                'category': 'clothing',
                'description': 'Comfortable 100% cotton t-shirt.',
                'price': 19.99,
                'variations': [
                    {'color': 'White', 'size': 'S', 'stock_quantity': 50},
                    {'color': 'White', 'size': 'M', 'stock_quantity': 75},
                    {'color': 'White', 'size': 'L', 'stock_quantity': 60},
                    {'color': 'Black', 'size': 'S', 'stock_quantity': 40},
                    {'color': 'Black', 'size': 'M', 'stock_quantity': 65},
                    {'color': 'Black', 'size': 'L', 'stock_quantity': 55}
                ]
            },
            {
                'name': 'Denim Jeans',
                'slug': 'denim-jeans',
                'category': 'clothing',
                'description': 'Classic denim jeans with perfect fit.',
                'price': 49.99,
                'variations': [
                    {'color': 'Blue', 'size': '30', 'stock_quantity': 40},
                    {'color': 'Blue', 'size': '32', 'stock_quantity': 50},
                    {'color': 'Blue', 'size': '34', 'stock_quantity': 45},
                    {'color': 'Black', 'size': '30', 'stock_quantity': 35},
                    {'color': 'Black', 'size': '32', 'stock_quantity': 45},
                    {'color': 'Black', 'size': '34', 'stock_quantity': 40}
                ]
            },
            {
                'name': 'Python Programming',
                'slug': 'python-programming',
                'category': 'books',
                'description': 'Comprehensive guide to Python programming.',
                'price': 39.99,
                'variations': [
                    {'color': None, 'size': 'Paperback', 'stock_quantity': 100},
                    {'color': None, 'size': 'Hardcover', 'stock_quantity': 50}
                ]
            },
            {
                'name': 'Coffee Maker',
                'slug': 'coffee-maker',
                'category': 'home-kitchen',
                'description': 'Automatic coffee maker with timer.',
                'price': 79.99,
                'variations': [
                    {'color': 'Black', 'size': None, 'stock_quantity': 75},
                    {'color': 'Silver', 'size': None, 'stock_quantity': 60}
                ]
            },
        ]

        # Create a placeholder image
        placeholder_path = os.path.join(settings.MEDIA_ROOT, 'products', 'images', 'placeholder.jpg')
        os.makedirs(os.path.dirname(placeholder_path), exist_ok=True)
        if not os.path.exists(placeholder_path):
            # Create a simple colored image using PIL
            from PIL import Image
            img = Image.new('RGB', (800, 800), color='purple')
            img.save(placeholder_path)

        for prod_data in products:
            category = Category.objects.get(slug=prod_data['category'])
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                slug=prod_data['slug'],
                category=category,
                defaults={
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                }
            )

            # Create product variations
            for var_data in prod_data.get('variations', []):
                ProductVariation.objects.get_or_create(
                    product=product,
                    color=var_data['color'],
                    size=var_data['size'],
                    defaults={
                        'stock_quantity': var_data['stock_quantity']
                    }
                )

            if created:
                # Add placeholder image
                with open(placeholder_path, 'rb') as f:
                    product.image.save(f'product_{product.id}.jpg', File(f), save=True)
                self.stdout.write(self.style.SUCCESS(f'Created product "{product.name}"'))

        self.stdout.write(self.style.SUCCESS('Successfully created sample data'))
