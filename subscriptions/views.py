from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from profiles.models import UserProfile

import stripe


def subscriptions(request):
    """ A view to return the subscriptions page """

    return render(request, 'subscriptions/subscriptions.html')


@login_required
def subscription_checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    try:
        if request.user.userprofile.membership:
            return redirect('profile')
    except UserProfile.DoesNotExist:
        pass

    if request.method == 'POST':
        stripe_customer = stripe.Customer.create(email=request.user.email, source=request.POST['stripeToken'])
        subscription = 'price_1IECPRC0y3iCJrXqNx7gE55o'
        if request.POST['subscription'] == 'yearly':
            subscription = 'price_1IECPRC0y3iCJrXqNVUpbMIA'

        subscription = stripe.Subscription.create(customer=stripe_customer.id,
        items=[{'plan': subscription}])

        customer = UserProfile.objects.get(user=request.user)
        customer.stripeid = stripe_customer.id
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = subscription.id
        customer.membership = True
        customer.save()

        return redirect('home')

    else:
        subscription = 'monthly'
        price = 6
        if request.method == 'GET' and 'subscription' in request.GET:
            if request.GET['subscription'] == 'yearly':
                subscription = 'yearly'
                price = '60'

        context = {
            'subscription': subscription,
            'price': price,
            'stripe_public_key': stripe_public_key,
        }

        return render(request, 'checkout/subscription_checkout.html', context)


def subscription_cancel(request):
    return render(request, 'checkout/subscription_cancel.html')


def subscription_success(reequest):
    return render(request, 'checkout/subscription_success.html')
