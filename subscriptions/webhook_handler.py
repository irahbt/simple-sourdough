from django.http import HttpResponse
from profiles.models import UserProfile


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)
   
def handle_checkout_session_completed(self, event):

    # Handle the checkout.session.completed event
    session = event['data']['object']

    session = stripe.checkout.Session.retrieve(request.GET['session_id'],)
    customer = UserProfile.objects.get(user=request.user)
    customer.stripeid = session.customer
    customer.membership = True
    customer.cancel_at_period_end = False
    customer.stripe_subscription_id = session.subscription
    customer.save()

    return HttpResponse(
        content=f'Webhook received: {event["type"]} | SUCCESS: Created subscription in webhook',
        status=200)


def handle_checkout_session_failed(self, event):
    """
    Handle the failed webhook from Stripe
    """
    return HttpResponse(
        content=f'Webhook received: {event["type"]}',
        status=200)