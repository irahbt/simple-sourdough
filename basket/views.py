from django.shortcuts import (
    render, redirect, reverse,
    HttpResponse, get_object_or_404)
from django.contrib import messages

from products.models import Product


def view_basket(request):
    """

    Returns:
    Basket contents page

    """

    return render(request, 'basket/basket.html')


def add_to_basket(request, item_id):
    """

    Add a quantity of the specified product to the shopping basket
    Prevent product amount from exceeding product inventory

    Returns:
    Url the request was made from

    """

    product = get_object_or_404(Product, pk=item_id)
    inventory = product.inventory
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    basket = request.session.get('basket', {})

    if product.has_inventory and inventory >= quantity:

        if item_id in list(basket.keys()):
            if inventory > basket[item_id]:
                basket[item_id] += quantity
                if not product.inventory_updated:
                    product.remove_items_from_inventory(
                        count=quantity, save=True)
                    product.inventory_updated = True
                messages.success(
                        request, f'{product.name} quantity has \
                        been updated to {basket[item_id]}')
            else:
                messages.error(request, f"Oh no, looks like there are only {inventory} {product.name} \
                            left in stock, \
                                please reduce your quantity to proceed.")
        else:
            basket[item_id] = quantity
            if not product.inventory_updated:
                product.remove_items_from_inventory(
                    count=quantity, save=True)
                product.inventory_updated = True
        messages.success(
                request, f'{product.name} has been added to your basket')
    else:
        messages.error(request, f"Oh no, looks like there are only {inventory} {product.name} \
                            left in stock, \
                                please reduce your quantity to proceed.")

    request.session['basket'] = basket
    return redirect(redirect_url)


def update_basket(request, item_id):
    """
    Update the quantity of the specified product to the specified amount.
    Prevent product amount from exceeding product inventory.

    Returns:
    Basket contents page

    """

    product = get_object_or_404(Product, pk=item_id)
    inventory = product.inventory
    quantity = int(request.POST.get('quantity'))
    basket = request.session.get('basket', {})

    if quantity > 0:
        if quantity <= inventory:
            basket[item_id] = quantity
            if not product.inventory_updated:
                product.remove_items_from_inventory(
                    count=quantity, save=True)
                product.inventory_updated = True
            messages.success(
                    request, f'{product.name} quantity \
                    has been updated to {basket[item_id]}')
        else:
            messages.error(request, f"Oh no, looks like there are only {inventory} {product.name} \
                            left in stock, \
                                please reduce your quantity to proceed.")
    else:
        for item_id, item_data in basket.items():
            print(item_data)
            if not product.inventory_updated:
                product.add_items_to_inventory(count=item_data, save=True)
                product.inventory_updated = True

        basket.pop(item_id)
        messages.success(
            request, f'{product.name} has been removed from your basket')

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))


def remove_from_basket(request, item_id):
    """

    Remove the item from the shopping basket

    Returns:
    Http Response

    """

    try:
        product = get_object_or_404(Product, pk=item_id)
        basket = request.session.get('basket', {})
        # quantity = int(request.get('quantity'))

        basket.pop(item_id)

        # basket[item_id] = quantity
        # if not product.inventory_updated:
        #     product.remove_items_from_inventory(
        #         count=quantity, save=True)
        #     product.inventory_updated = True
        # print(quantity)
        messages.success(
            request, f'{product.name} has been removed from your basket')

        request.session['basket'] = basket
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}, please try again')
        return HttpResponse(status=500)
