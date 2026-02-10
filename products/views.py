from django.shortcuts import render
from .models import Product


def product_list(request):

    products = Product.objects.filter(stock__gt=0)

    return render(request, "products/list.html", {
        "products": products
    })