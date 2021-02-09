from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


from profiles.models import UserProfile

import stripe


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


def subscriptions(request):
    """ A view to return the subscriptions page """

    return render(request, 'subscriptions/subscriptions.html')


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
            success_url='https://8000-c258c6d1-b0ff-4fce-b6f4-eb72b8f7ec16.ws-eu03.gitpod.io/subscriptions/subscription_success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://8000-c258c6d1-b0ff-4fce-b6f4-eb72b8f7ec16.ws-eu03.gitpod.io/subscriptions/subscription_cancel',
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


@csrf_exempt
def subscription_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_SUB_WH_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        session = stripe.checkout.Session.retrieve(request.GET['session_id'],)
        customer = UserProfile.objects.get(user=request.user)
        customer.stripeid = session.customer
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = session.subscription
        customer.save()

    return HttpResponse(status=200)