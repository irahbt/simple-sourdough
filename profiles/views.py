from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order
from recipes.models import Recipe

import stripe


@login_required
def profile(request):
    """

    Retrieve:
    Current user
    Newest recipe added
    User profile form information and save
    Orders associated with profile

    Returns:
    Individual profile page with profile form, orders and latest recipe

    """

    profile = get_object_or_404(UserProfile, user=request.user)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    latest_recipe = Recipe.objects.latest('added_date')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your information has been updated')
        else:
            messages.error(request, 'Update failed, \
                Please check form is valid.')

    orders = profile.orders.all
    form = UserProfileForm(instance=profile)
    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'latest_recipe': latest_recipe,
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


def order_history(request, order_number):
    """
    Retrieve individual orders

    Returns:
    Checkout success page with specified order

    """
    order = get_object_or_404(Order, order_number=order_number)
    messages.info(request, f'Order confirmation for {order_number}.')
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
