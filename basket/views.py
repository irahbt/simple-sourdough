from django.shortcuts import (
    render, redirect, reverse,
    HttpResponse, get_object_or_404)
from django.contrib import messages

from products.models import Product
 

def view_basket(request):
    """ A view to return the basket contents page """

    return render(request, 'basket/basket.html')


def add_to_basket(request, item_id):
    """ Add a quantity of the specified product to the shopping basket """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    colour = None
    if 'product_colour' in request.POST:
        colour = request.POST['product_colour']

    basket = request.session.get('basket', {})

    if colour:
        if item_id in list(basket.keys()):
            if colour in basket[item_id]['items_by_colour'].keys():
                basket[item_id]['items_by_colour'][colour] += quantity
                messages.success(
                    request, f'{colour.capitalize()} {product.name} quantity has been updated to {basket[item_id]["items_by_colour"][colour]}')

            else:
                basket[item_id]['items_by_colour'][colour] = quantity
                messages.success(
                    request, f'{colour.capitalize()} {product.name} has been added to your basket')

        else:
            basket[item_id] = {'items_by_colour': {colour: quantity}}
            messages.success(
                request, f'{colour.capitalize()} {product.name} has been added to your basket')

    else:
        if item_id in list(basket.keys()):
            basket[item_id] += quantity
            messages.success(
                    request, f'{product.name} quantity has been updated to {basket[item_id]}')

        else:
            basket[item_id] = quantity
            messages.success(request, f'{product.name} has been added to your basket')

    request.session['basket'] = basket
    return redirect(redirect_url)


def update_basket(request, item_id):
    """Update the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    colour = None
    if 'product_colour' in request.POST:
        colour = request.POST['product_colour']
    basket = request.session.get('basket', {})

    if colour:
        if quantity > 0:
            basket[item_id]['items_by_colour'][colour] = quantity
            messages.success(
                    request, f'{colour.capitalize()} {product.name} quantity has been updated to {basket[item_id]["items_by_colour"][colour]}')
        else:
            del basket[item_id]['items_by_colour'][colour]
            if not basket[item_id]['items_by_colour']:
                basket.pop(item_id)
            messages.success(
                request, f'{colour.capitalize()} {product.name} has been removed from your basket')

    else:
        if quantity > 0:
            basket[item_id] = quantity
            messages.success(
                    request, f'{product.name} quantity has been updated to {basket[item_id]}')
        else:
            basket.pop(item_id)
            messages.success(
                request, f'{product.name} has been removed from your basket')

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))


def remove_from_basket(request, item_id):
    """Remove the item from the shopping basket"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        colour = None
        if 'product_colour' in request.POST:
            colour = request.POST['product_colour']
        basket = request.session.get('basket', {})

        if colour:
            del basket[item_id]['items_by_colour'][colour]
            if not basket[item_id]['items_by_colour']:
                basket.pop(item_id)
            messages.success(
                request, f'{colour.capitalize()} {product.name} has been removed from your basket')
        else:
            basket.pop(item_id)
            messages.success(
                request, f'{product.name} has been removed from your basket')

        request.session['basket'] = basket
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}, please try again')
        return HttpResponse(status=500)