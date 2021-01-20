from django.shortcuts import render, redirect, reverse, HttpResponse


def view_basket(request):
    """ A view to return the basket contents page """

    return render(request, 'basket/basket.html')


def add_to_basket(request, item_id):
    """ Add a quantity of the specified product to the shopping basket """

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

            else:
                basket[item_id]['items_by_colour'][colour] = quantity

        else:
            basket[item_id] = {'items_by_colour': {colour: quantity}}

    else:
        if item_id in list(basket.keys()):
            basket[item_id] += quantity
        else:
            basket[item_id] = quantity

    request.session['basket'] = basket
    return redirect(redirect_url)


def update_basket(request, item_id):
    """Update the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    colour = None
    if 'product_colour' in request.POST:
        colour = request.POST['product_colour']
    basket = request.session.get('basket', {})

    if colour:
        if quantity > 0:
            basket[item_id]['items_by_colour'][colour] = quantity
        else:
            del basket[item_id]['items_by_colour'][colour]
            if not basket[item_id]['items_by_colour']:
                basket.pop(item_id)
    else:
        if quantity > 0:
            basket[item_id] = quantity
        else:
            basket.pop(item_id)

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))


def remove_from_basket(request, item_id):
    """Remove the item from the shopping basket"""

    try:
        colour = None
        if 'product_colour' in request.POST:
            colour = request.POST['product_colour']
        basket = request.session.get('basket', {})

        if colour:
            del basket[item_id]['items_by_colour'][colour]
            if not basket[item_id]['items_by_colour']:
                basket.pop(item_id)
        else:
            basket.pop(item_id)

        request.session['basket'] = basket
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)