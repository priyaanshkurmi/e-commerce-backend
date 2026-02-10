from products.models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")

        if not cart:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, product_id, qty=1):
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = 0

        self.cart[product_id] += qty
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session["cart"] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def items(self):
        products = Product.objects.filter(id__in=self.cart.keys())

        result = []

        for product in products:
            qty = self.cart[str(product.id)]

            result.append({
                "product": product,
                "quantity": qty,
                "price": product.price,
                "total": product.price * qty
            })

        return result

    def get_total_price(self):
        return sum(item["total"] for item in self.items())