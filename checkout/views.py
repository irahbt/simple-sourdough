from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from basket.contexts import basket_contents

import stripe


def checkout(request):
    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, "There's nothing in your basket right now")
        return redirect(reverse('products'))
    
    current_basket = basket_contents
    total = current_basket['grand_total']
    stripe_total = round(total * 100)
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51HvgcNC0y3iCJrXqhi04GCxf5kYhgPvHlcXuO2kaigKKurbsieGPc9GgdJ63XTLBmvAD9nIeyC1Qyml16AXHUouf00ogCGCDbc'
    }

    return render(request, template, context)
