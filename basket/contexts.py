from django.conf import settings


def basket_contents(request):

    basket_items = []
    total = 0
    product_count = 0

    if total < settings.FREE_SHIPPING_THRESHOLD:
        shipping = settings.STANDARD_SHIPPING
        free_shipping_delta = settings.FREE_SHIPPING_THRESHOLD - total
    else:
        shipping = 0
        free_shipping_delta = 0

    grand_total = shipping + total

    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'shipping': shipping,
        'free_shipping_delta': free_shipping_delta,
        'free_shipping_threshold': settings.FREE_SHIPPING_THRESHOLD,
        'grand_total': grand_total,
    }

    return context