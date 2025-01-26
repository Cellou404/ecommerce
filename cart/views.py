from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Cart, CartItem

# Create your views here.

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {
        'cart': cart
    })

@login_required
def cart_count(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_count = cart.items.count()
    return render(request, 'cart/partials/cart_count.html', {
        'cart_count': cart_count
    })

@login_required
def cart_total(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    total = float(cart.get_total_price())
    return HttpResponse(f'${total:.2f}')

@login_required
@require_POST
def cart_add(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id, available=True)
    
    # Get variation details from form
    color = request.POST.get('color')
    size = request.POST.get('size')
    quantity = int(request.POST.get('quantity', 1))
    
    # Find the specific variation
    variation = product.variations.filter(
        color=color if color else None, 
        size=size if size else None
    ).first()
    
    if not variation or variation.stock_quantity < quantity:
        messages.error(request, 'Selected variation is out of stock.')
        return redirect(product.get_absolute_url())
    
    # Create or update cart item with variation details
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        color=color,
        size=size,
        defaults={'quantity': quantity}
    )
    
    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()
    
    # Optionally, update the variation's stock
    variation.stock_quantity -= quantity
    variation.save()
    
    messages.success(request, f'{product.name} was added to your cart.')
    
    if request.htmx:
        return render(request, 'cart/partials/cart_count.html', {
            'cart_count': cart.items.count()
        })
    return redirect('cart:cart_detail')

@login_required
@require_POST
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        messages.success(request, f'{product.name} was removed from your cart.')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item was not in your cart.')
    
    if request.htmx:
        return render(request, 'cart/partials/cart_count.html', {
            'cart_count': cart.items.count()
        })
    return redirect('cart:cart_detail')

@login_required
@require_POST
def cart_update_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get('action')
    
    if action == 'increment':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrement':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            if request.htmx:
                response = HttpResponse("")
                response['HX-Trigger'] = 'cartUpdate'
                return response
            return redirect('cart:cart_detail')
    
    if request.htmx:
        response = render(request, 'cart/partials/cart_item.html', {
            'item': cart_item
        })
        response['HX-Trigger'] = 'cartUpdate'
        return response
    
    return redirect('cart:cart_detail')
