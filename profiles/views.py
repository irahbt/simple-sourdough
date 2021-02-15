from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django import template

from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order
from recipes.models import Recipe

from datetime import datetime

import stripe


def profile(request):
    """ Display the user's profile. """

    profile = get_object_or_404(UserProfile, user=request.user)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    subscription = stripe.Subscription.retrieve(
        request.user.userprofile.stripe_subscription_id)

    latest_recipe = Recipe.objects.latest('added_date')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your information has been updated')
        else:
            messages.error(request, 'Update failed, Please check form is valid.')

    orders = profile.orders.all
    form = UserProfileForm(instance=profile)
    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'subscription': subscription,
        'latest_recipe': latest_recipe,
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


def subscription_settings(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    subscription = stripe.Subscription.retrieve(
        request.user.userprofile.stripe_subscription_id)
    membership = False
    cancel_at_period_end = False
    # period_end code adapted from
    # https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date
    period_end = datetime.utcfromtimestamp(
        int(subscription.current_period_end)).strftime('%d-%m-%y')
    amount = subscription.plan.amount / 100
 
    if request.method == 'POST':
        subscription.cancel_at_period_end = True
        request.user.userprofile.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.userprofile.save()
    else:
        try:
            if request.user.userprofile.membership:
                membership = True
            if request.user.userprofile.cancel_at_period_end:
                cancel_at_period_end = True
        except UserProfile.DoesNotExist:
            membership = False

    template = 'profiles/subscription_settings.html'
    context = {
        'subscription': subscription,
        'membership': membership,
        'cancel_at_period_end': cancel_at_period_end,
        'amount': amount,
        'period_end': period_end,
    }
    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    messages.info(request, f'Order confirmation for {order_number}.')
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
