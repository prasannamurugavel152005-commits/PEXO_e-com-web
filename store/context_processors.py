from .cart import FREE_SHIPPING_THRESHOLD, cart_count
from .models import Category


def cart_summary(request):
    return {
        'cart_count': cart_count(request),
        'nav_categories': Category.objects.all()[:5],
        'free_shipping_threshold': FREE_SHIPPING_THRESHOLD,
    }