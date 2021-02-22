from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponse
from django.conf import settings
from datetime import datetime

from profiles.models import UserProfile

import stripe


def subscriptions(request):
    """ A view to return the subscription page """
    return render(request, 'subscriptions/subscriptions.html')


@user_passes_test(lambda u: u.is_superuser)
def update_accounts(request):
    """
    A view to allow superuser to update/cancel user's
    membership if their subscription is inactive.
    """
    profiles = UserProfile.objects.all()
    for profile in profiles:
        subscription = stripe.Subscription.retrieve(
            profile.stripe_subscription_id)
        if subscription.status != 'active':
            profile.membership = False
        else:
            profile.membership = True
        profile.cancel_at_period_end = subscription.cancel_at_period_end
        profile.save()
        return HttpResponse('Subscriptions update completed')


@login_required
def subscription_checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        if request.user.userprofile.membership:
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
            line_items=[{
                'price': subscription_id,
                'quantity': 1,
                }],
            mode='subscription',
            allow_promotion_codes=True,
            success_url='https://8000-turquoise-earthworm-f1kwkeby.ws-eu03.gitpod.io/subscriptions/subscription_success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://8000-turquoise-earthworm-f1kwkeby.ws-eu03.gitpod.io/subscriptions/subscription_cancel',
        )

        template = 'subscriptions/subscription_checkout.html'
        context = {
            'final_pound': final_pound,
            'session_id': session.id,
            'subscription': subscription,
        }

        return render(request, template, context)


def subscription_cancel(request):
    return render(request, 'subscriptions/subscription_cancel.html')


def subscription_success(request):

    # if request.method == 'GET' and 'session_id' in request.GET:
    #     session = stripe.checkout.Session.retrieve(request.GET['session_id'],)
    #     customer = UserProfile.objects.get(user=request.user)
    #     customer.stripeid = session.customer
    #     customer.membership = True
    #     customer.cancel_at_period_end = False
    #     customer.stripe_subscription_id = session.subscription
    #     customer.save()

    return render(request, 'subscriptions/subscription_success.html')


def subscription_settings(request):
    """
    A view to allow the user to view their subscription settings
    and cancel membership.
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
