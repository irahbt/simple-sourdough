from django.shortcuts import (
    render, redirect, reverse,
    get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from basket.contexts import basket_contents

import stripe
import json


@require_POST
def cache_checkout_data(request):
    """
    Retrieve post checkout data

    Returns:
    Http Response

    """

    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
            'status': '',
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later or get in touch')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """

    Retrieve order form data
    Retrieve basket contents and create order line item(s)
    Create Stripe payment intent

    Returns:
    Checkout page, stripe public key and individual payment intent

    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        basket = request.session.get('basket', {})
        pid = request.POST.get('client_secret').split('_secret')[0]

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            }

        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_basket = json.dumps(basket)
            order.save()

            for item_id, item_data in basket.items():
                try:
                    product = get_object_or_404(Product, id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()

                    if not product.inventory_updated:
                        product.remove_items_from_inventory(
                            count=item_data, save=True)
                        product.inventory_updated = True

                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your basket \
                            wasn't found in our database."
                        "Please contact us for assistance")
                    )
                    order.delete()
                    return redirect(reverse('view_basket'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse(
                'checkout_success', args=[order.order_number]))

        else:
            messages.error(request, 'There was an error in your form. \
                Please double check your information.')

    else:
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "There's nothing in your basket right now")
            return redirect(reverse('products'))

        for item_id, item_data in basket.items():
            product = get_object_or_404(Product, id=item_id)
            inventory = product.inventory
            if not product.has_inventory():
                messages.error(request, f"Oh no, looks like {product.name} \
                    has very recently sold out. \
                        Please remove from your basket to proceed.")
                return redirect(reverse('view_basket'))
            if inventory < item_data:
                messages.error(request, f"Oh no, looks like there are only {inventory} \
                    {product.name}. \
                        Left in stock, please alter your basket to proceed.")
                return redirect(reverse('view_basket'))

        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Try to prefill the form with saved info
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'town_or_city': profile.default_town_or_city,
                    'county': profile.default_county,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                })

            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """

    Handle successful checkouts

    Returns:
    Checkout success page with order details attached

    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)

        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_town_or_city': order.town_or_city,
                'default_county': order.county,
                'default_country': order.country,
                'default_postcode': order.postcode,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Your order has been recieved. \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'basket' in request.session:
        del request.session['basket']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
