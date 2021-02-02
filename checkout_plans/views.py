from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from profiles.models import UserProfile

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout_plan(request):

    if request.method == 'POST':
        stripe_customer = stripe.Customer.create(email=request.user.email, source=request.POST['stripeToken'])
        plan = 'price_1IECPRC0y3iCJrXqNx7gE55o'
        if request.POST['plan'] == 'yearly':
            plan = 'price_1IECPRC0y3iCJrXqNVUpbMIA'

        subscription = stripe.Subscription.create(customer=stripe_customer.id,
        items=[{'plan':plan}])

        return redirect('home')

    else:
        plan = 'monthly'
        price = 6
        if request.method == 'GET' and 'plan' in request.GET:
            if request.GET['plan'] == 'yearly':
                plan = 'yearly'
                price = '60'

        context = {
            'plan': plan,
            'price': price,
        }

        return render(request, 'checkout_plans/checkout_plan.html', context)

