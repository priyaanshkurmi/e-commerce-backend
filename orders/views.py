from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from products.models import Product
from .cart import Cart
from .models import Order, OrderItem
from .invoice import generate_invoice_pdf


def add_to_cart(request, product_id):
    cart = Cart(request)
    # Support adding from multiple places. If a `next` POST parameter
    # is provided (or HTTP_REFERER exists) we redirect back there so
    # the UX can remain on the product list; otherwise go to cart.
    quantity = int(request.POST.get('quantity', 1)) if request.method == 'POST' else 1
    cart.add(product_id, quantity)

    # Prefer explicit next parameter, then referer, else cart
    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER')
    # Ensure next_url is internal (basic safety): only allow paths starting with '/'
    if next_url and isinstance(next_url, str) and next_url.startswith('/'):
        return redirect(next_url)

    return redirect("cart_detail")


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect("cart_detail")


def cart_detail(request):
    cart = Cart(request)

    return render(request, "orders/cart.html", {
        "cart": cart
    })


@login_required
def checkout(request):
    from accounts.models import Address
    from django.contrib import messages
    
    cart = Cart(request)
    
    # Check if user has a shipping address
    address = Address.objects.filter(user=request.user).first()
    
    if request.method == "POST":
        # Validate that address exists before creating order
        if not address:
            messages.error(request, 'Please add a shipping address before checkout.')
            return redirect('manage_address')
        
        if not cart.items():
            messages.error(request, 'Your cart is empty.')
            return redirect('cart_detail')

        order = Order.objects.create(
            user=request.user,
            total_price=cart.get_total_price()
        )

        for item in cart.items():
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                price=item["price"],
                quantity=item["quantity"]
            )

            # Reduce stock
            product = item["product"]
            product.stock -= item["quantity"]
            product.save()

        cart.clear()

        return redirect("start_payment", order_id=order.id)

    return render(request, "orders/checkout.html", {
        "cart": cart,
        "address": address
    })


@login_required
def download_invoice(request, order_id):
    """Download order invoice as PDF"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return generate_invoice_pdf(order)