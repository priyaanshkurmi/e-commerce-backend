from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from products.models import Product
from .cart import Cart
from .models import Order, OrderItem


def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

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

        return render(request, "orders/success.html", {
            "order": order
        })

    return render(request, "orders/checkout.html", {
        "cart": cart
    })