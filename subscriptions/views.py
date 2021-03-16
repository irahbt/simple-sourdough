from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponse
from django.contrib import messages
from django.conf import settings
from datetime import datetime

from profiles.models import UserProfile

import stripe


def subscriptions(request):
    """

    Returns:
    Subscriptions page

    """
    return render(request, 'subscriptions/subscriptions.html')


@user_passes_test(lambda u: u.is_superuser)
def update_accounts(request):
    """

    A view to update the membership status of all accounts
    Retrieve user profile
    Retrieve stripe subscriptions
    Check subscription status
    Save profile

    Returns:
    Http response

    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    profiles = UserProfile.objects.all()
    for profile in profiles:
        if profile.membership:
            subscription = stripe.Subscription.retrieve(
                profile.stripe_subscription_id)
            if subscription.status != 'active':
                profile.membership = False
                profile.stripe_customer_id = ""
                profile.stripe_subscription_id = ""

            else:
                profile.membership = True
            profile.cancel_at_period_end = subscription.cancel_at_period_end
            profile.save()
            return HttpResponse('Memberships update completed')
        

@login_required
def subscription_checkout(request):
    """

    Ensure user has a profile and without memeberhsip attached
    Retrieve subscription type
    Create stripe checkout session

    Returns:
    Subscription checkout page with final pound, session id and subscription

    """

    stripe.api_key = settings.STRIPE_SECRET_KEY
    domain_url = settings.DOMAIN_URL

    try:
        if request.user.userprofile.membership:
            messages.success(request, 'You already have an ongoing membership, \
                manage your settings here.')
            return redirect('profile')
    except UserProfile.DoesNotExist:
        pass

    if request.method == 'POST':
        pass
    else:
        subscription = 'monthly'
        subscription_id = 'price_1IMBPUC0y3iCJrXqtD6J5WjI'
        final_pound = 2.50

        if request.method == 'GET' and 'subscription' in request.GET:
            if request.GET['subscription'] == 'yearly':
                subscription = 'yearly'
                subscription_id = 'price_1IMBPgC0y3iCJrXquYi3X9fs'
                final_pound = 25.00

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=request.user.email,
            client_reference_id=request.user.id,
            line_items=[{
                'price': subscription_id,
                'quantity': 1,
                }],
            mode='subscription',
            allow_promotion_codes=True,
            success_url=(domain_url + 'subscriptions/subscription_success?session_id={CHECKOUT_SESSION_ID}'),
            cancel_url=(domain_url + 'subscriptions/subscription_cancel'),
        )

        template = 'subscriptions/subscription_checkout.html'
        context = {
            'final_pound': final_pound,
            'session_id': session.id,
            'subscription': subscription,
        }

        return render(request, template, context)


def subscription_cancel(request):
    """

    Returns:
    Subscription cancelled page

    """
    return render(request, 'subscriptions/subscription_cancel.html')


def subscription_success(request):
    """

    Returns:
    Subscription success page

    """
    return render(request, 'subscriptions/subscription_success.html')


def subscription_settings(request):
    """

    Retrieve stripe subscription information for current user profile
    If request change cancel at period end to true where necessary and save

    Returns:
    Subscription settings page with associated subscription information

    """
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

    template = 'subscriptions/subscription_settings.html'
    context = {
        'subscription': subscription,
        'membership': membership,
        'cancel_at_period_end': cancel_at_period_end,
        'amount': amount,
        'period_end': period_end,
    }
    return render(request, template, context)
