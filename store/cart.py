from decimal import Decimal

from .models import Product

FREE_SHIPPING_THRESHOLD = Decimal('999.00')
STANDARD_SHIPPING = Decimal('49.00')


def cart_count(request):
    return sum(int(quantity) for quantity in request.session.get('cart', {}).values())


def cart_items(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(pk__in=cart.keys(), available=True).select_related('category')
    items = []
    for product in products:
        quantity = min(int(cart.get(str(product.pk), 0)), product.stock)
        if quantity > 0:
            items.append({'product': product, 'quantity': quantity, 'line_total': product.price * quantity})
    return items