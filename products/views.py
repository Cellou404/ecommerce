from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, ProductVariation
from django.db.models import Q

# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # Check for category slug in URL path
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Check for category in query parameter
    category_query = request.GET.get('category', '')
    if category_query:
        category = get_object_or_404(Category, slug=category_query)
        products = products.filter(category=category)
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Check if it's an HTMX request
    if request.headers.get('HX-Request'):
        return render(request, 'products/product_list_partial.html', {
            'category': category,
            'categories': categories,
            'products': products,
            'search_query': search_query,
            'category_query': category_query
        })
    
    return render(request,
        'products/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
            'search_query': search_query,
            'category_query': category_query
        }
    )

def product_detail(request, category_slug, slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=slug, available=True)
    
    # Get all variations for the product
    variations = product.variations.all()
    
    # Group variations by color and size
    color_variations = set(variations.values_list('color', flat=True).distinct())
    size_variations = set(variations.values_list('size', flat=True).distinct())
    
    # Remove None from variations if present
    color_variations = {c for c in color_variations if c is not None}
    size_variations = {s for s in size_variations if s is not None}
    
    return render(request,
        'products/detail.html',
        {
            'category': category, 
            'product': product,
            'variations': variations,
            'color_variations': color_variations,
            'size_variations': size_variations,
        }
    )
