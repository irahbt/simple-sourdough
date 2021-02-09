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
        pass
    else:
        subscription = 'monthly'
        subscription_id = 'price_1IIt2jC0y3iCJrXqFs8IMEzd'
        final_pound = 3.99

        if request.method == 'GET' and 'subscription' in request.GET:
            if request.GET['subscription'] == 'yearly':
                subscription = 'yearly'
                subscription_id = 'price_1IIt2uC0y3iCJrXqY47vRnG0'
                final_pound = 39.99

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=request.user.email,
            line_items=[{
                'price': subscription_id,
                'quantity': 1,
                }],
            mode='subscription',
            allow_promotion_codes=True,
            success_url='http://127.0.0.1:8000/subscription_success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/subscription_cancel',
        )

        template = 'checkout/subscription_checkout.html'
        context = {
            'final_pound': final_pound,
            'session_id': session.id,
        }

        return render(request, template, context)


def subscription_cancel(request):
    return render(request, 'checkout/subscription_cancel.html')


def subscription_success(request):

    if request.method == 'GET' and 'session_id' in request.GET:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'],)
        customer = UserProfile.objects.get(user=request.user)
        customer.stripeid = session.customer
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = session.subscription
        customer.save()

    return render(request, 'checkout/subscription_success.html')
