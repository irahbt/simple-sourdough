from django.shortcuts import (
    render, redirect, reverse,
    HttpResponse, get_object_or_404)
from django.contrib import messages

from products.models import Product
from subscriptions.models import SubscriptionPlan

 

def view_basket(request):
    """ A view to return the basket contents page """

    return render(request, 'basket/basket.html')


def add_to_basket(request, item_id, category):
    """ Add a quantity of the specified product to the shopping basket """

    redirect_url = request.POST.get('redirect_url')
    colour = None
    if 'product_colour' in request.POST:
        colour = request.POST['product_colour']

    basket = request.session.get('basket', {'product': {},
                                            'subscription': {}})

    if category == 'product':
        quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Product, pk=item_id)
        if colour:
            if item_id in list(basket[category].keys()):
                if colour in basket[category][item_id]['items_by_colour'].keys():
                    basket[category][item_id]['items_by_colour'][colour] += quantity
                    messages.success(
                        request, f'{colour.capitalize()} {product.name} quantity has been updated to {basket[category][item_id]["items_by_colour"][colour]}')
                else:
                    basket[category][item_id]['items_by_colour'][colour] = quantity
                    messages.success(
                        request, f'{colour.capitalize()} {product.name} has been added to your basket')
            else:
                basket[category][item_id] = {'items_by_colour': {colour: quantity}}
                messages.success(
                    request, f'{colour.capitalize()} {product.name} has been added to your basket')
        else:
            if item_id in list(basket[category].keys()):
                basket[category][item_id] += quantity
                messages.success(
                        request, f'{product.name} quantity has been updated to {basket[category][item_id]}')
            else:
                basket[category][item_id] = quantity
                messages.success(request, f'{product.name} has been added to your basket')

    elif category == 'subscription':
        quantity = 1
        plan = get_object_or_404(SubscriptionPlan, pk=item_id)
        if item_id in list(basket[category].keys()):
            messages.success(
                    request, f'You already have a subscription plan in your basket, head to basket to remove')
        else:
            basket[category][item_id] = quantity
            messages.success(request, f'{plan.name} subscription plan has been added to your basket')

    request.session['basket'] = basket
    return redirect(redirect_url)


def update_basket(request, item_id, category):
    """Update the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    colour = None
    if 'product_colour' in request.POST:
        colour = request.POST['product_colour']
    
    basket = request.session.get('basket', {'product': {},
                                            'subscription': {}})
    if category == 'product':
        product = get_object_or_404(Product, pk=item_id)
        if colour:
            if quantity > 0:
                basket[category][item_id]['items_by_colour'][colour] = quantity
                messages.success(
                        request, f'{colour.capitalize()} {product.name} quantity has been updated to {basket[category][item_id]["items_by_colour"][colour]}')
            else:
                del basket[category][item_id]['items_by_colour'][colour]
                if not basket[category][item_id]['items_by_colour']:
                    del basket[category][item_id]
                messages.success(
                    request, f'{colour.capitalize()} {product.name} has been removed from your basket')
        else:
            if quantity > 0:
                basket[category][item_id] = quantity
                messages.success(
                        request, f'{product.name} quantity has been updated to {basket[category][item_id]}')
            else:
                del basket[category][item_id]
                messages.success(
                    request, f'{product.name} has been removed from your basket')

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))


def remove_from_basket(request, item_id, category):
    """Remove the item from the shopping basket"""
    colour = None
    if 'product_colour' in request.POST:
        colour = request.POST['product_colour']
    basket = request.session.get('basket', {'product': {},
                                            'subscription': {}})
    try:
        if category == 'product':
            product = get_object_or_404(Product, pk=item_id)
            if colour:
                del basket[category][item_id]['items_by_colour'][colour]
                if not basket[category][item_id]['items_by_colour']:
                    del basket[category][item_id]
                messages.success(
                    request, f'{colour.capitalize()} {product.name} has been removed from your basket')
            else:
                del basket[category][item_id]
                messages.success(
                    request, f'{product.name} has been removed from your basket')

        elif category == 'subscription':
            plan = get_object_or_404(SubscriptionPlan, pk=item_id)
            del basket[category][item_id]
            messages.success(
                request, f'{plan.name} has been removed from your basket')

        request.session['basket'] = basket
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}, please try again')
        return HttpResponse(status=500)
