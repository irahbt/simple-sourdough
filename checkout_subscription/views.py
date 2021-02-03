from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from profiles.models import UserProfile

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout_subscription(request):
    
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
        }

        return render(request, 'checkout_subscription/checkout_subscription.html', context)

