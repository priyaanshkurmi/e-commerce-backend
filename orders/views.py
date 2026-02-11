from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from products.models import Product
from .cart import Cart
from .models import Order, OrderItem
from .invoice import generate_invoice_pdf


def add_to_cart(request, product_id):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1)) if request.method == 'POST' else 1
    cart.add(product_id, quantity)

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
    cart = Cart(request)

    if request.method == "POST":

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
        "cart": cart
    })


@login_required
def download_invoice(request, order_id):
    """Download order invoice as PDF"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return generate_invoice_pdf(order)