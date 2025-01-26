from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product

# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
        'products/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products
        }
    )

def product_detail(request, category_slug, slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request,
        'products/detail.html',
        {'category': category, 'product': product,}
    )
