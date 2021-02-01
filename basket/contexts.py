from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from subscriptions.models import SubscriptionPlan

from decimal import Decimal


def basket_contents(request):

    basket_items = []
    total = 0
    product_count = 0
    basket = request.session.get('basket', {'product': {},
                                            'subscription': {}})
    if bool(basket['product']):
        for item_id, item_data in basket['product'].items():
            if isinstance(item_data, int):
                product = get_object_or_404(Product, pk=item_id)
                total += item_data * product.price
                product_count += item_data
                basket_items.append({
                    'item_id': item_id,
                    'quantity': item_data,
                    'product': product,
                })
            else:
                product = get_object_or_404(Product, pk=item_id)
                for colour, quantity in item_data['items_by_colour'].items():
                    total += quantity * product.price
                    product_count += quantity
                    basket_items.append({
                        'item_id': item_id,
                        'quantity': quantity,
                        'product': product,
                        'colour': colour,
                    })

    if bool(basket['subscription']):
        shipping = 0
        free_shipping_delta = 0
        for item_id, item_data in basket['subscription'].items():
            if isinstance(item_data, int):
                plan = get_object_or_404(SubscriptionPlan, pk=item_id)
                total += item_data * plan.price
                product_count += item_data
                basket_items.append({
                    'item_id': item_id,
                    'plan': plan,
                })

    if bool(basket['product']) and total < settings.FREE_SHIPPING_THRESHOLD:
        shipping = Decimal(settings.STANDARD_SHIPPING)
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