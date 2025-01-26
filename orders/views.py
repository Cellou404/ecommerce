from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm

# Create your views here.

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {
        'orders': orders
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {
        'order': order
    })

@login_required
def order_create(request):
    cart = Cart.objects.get(user=request.user)
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()

            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    price=cart_item.product.price,
                    quantity=cart_item.quantity
                )

            # Clear the cart
            cart.items.all().delete()
            messages.success(request, 'Order placed successfully!')
            return redirect('orders:order_detail', order_id=order.id)
    else:
        # Pre-fill the form with user information
        initial_data = {}
        if hasattr(request.user, 'email'):
            initial_data['email'] = request.user.email
        form = OrderCreateForm(initial=initial_data)

    return render(request, 'orders/create.html', {
        'form': form,
        'cart': cart
    })
