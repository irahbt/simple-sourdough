from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm
from plans.models import RecipePlan
from checkout.models import Order

import stripe


def profile(request):
    """ Display the user's profile. """

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your information has been updated')

    orders = profile.orders.all
    plans = RecipePlan.objects
    form = UserProfileForm(instance=profile)
    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'form': form,
        'orders': orders,
        'on_profile_page': True,
        'plans': plans,
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


def membership_settings(request):
    membership = False
    cancel_at_period_end = False
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.userprofile.stripe_subscription_id)
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

    template = 'profiles/membership_settings.html'
    context = {
        'membership': membership,
        'cancel_at_period_end': cancel_at_period_end,
    }
    return render(request, template, context)
