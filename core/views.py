from django.shortcuts import render
from products.models import Category, Product


def home(request):
    categories = Category.objects.all()[:4]
    featured_products = Product.objects.filter(available=True)[:8]
    
    return render(request, 'core/home.html', {
        'categories': categories,
        'featured_products': featured_products,
    })


def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    return render(request, 'errors/500.html', status=500)
