from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from products.models import Category, Product
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
            },
            {
                'name': 'Wireless Headphones',
                'slug': 'wireless-headphones',
                'category': 'electronics',
                'description': 'Premium wireless headphones with noise cancellation.',
                'price': 199.99,
            },
            {
                'name': 'Cotton T-Shirt',
                'slug': 'cotton-t-shirt',
                'category': 'clothing',
                'description': 'Comfortable 100% cotton t-shirt.',
                'price': 19.99,
            },
            {
                'name': 'Denim Jeans',
                'slug': 'denim-jeans',
                'category': 'clothing',
                'description': 'Classic denim jeans with perfect fit.',
                'price': 49.99,
            },
            {
                'name': 'Python Programming',
                'slug': 'python-programming',
                'category': 'books',
                'description': 'Comprehensive guide to Python programming.',
                'price': 39.99,
            },
            {
                'name': 'Coffee Maker',
                'slug': 'coffee-maker',
                'category': 'home-kitchen',
                'description': 'Automatic coffee maker with timer.',
                'price': 79.99,
            },
        ]

        # Create a placeholder image
        placeholder_path = os.path.join(settings.MEDIA_ROOT, 'products', 'images', 'placeholder.jpg')
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
                    'available': True,
                }
            )
            
            if created:
                # Add placeholder image
                with open(placeholder_path, 'rb') as f:
                    product.image.save(f'product_{product.id}.jpg', File(f), save=True)
                self.stdout.write(self.style.SUCCESS(f'Created product "{product.name}"'))

        self.stdout.write(self.style.SUCCESS('Successfully created sample data'))
