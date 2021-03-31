from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User

from checkout.models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'emails/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'emails/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def _send_confirmation_email_subscription(self, profile):
        """Send the user a confirmation email"""
        cust_email = profile.user.email
        subject = render_to_string(
            'emails/confirmation_emails/confirmation_email_subject_subscription.txt',
            {'profile': profile})
        body = render_to_string(
            'emails/confirmation_emails/confirmation_email_body_subscription.txt',
            {'profile': profile, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_checkout_session_completed(self, event):
        session = event.data.object

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Get the user
        user = User.objects.get(id=client_reference_id)

        # Get user profile and update
        profile = get_object_or_404(UserProfile, user=user)
        profile.stripe_customer_id = stripe_customer_id
        profile.stripe_subscription_id = stripe_subscription_id
        profile.cancel_at_period_end = False
        profile.membership = True
        profile.save()

        self._send_confirmation_email_subscription(profile)
        return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: \
                        Created subscription in webhook',
                    status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        customer = intent.get('customer')

        if customer:
            return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: \
                        Created order in webhook',
                    status=200)

        else:
            basket = intent.metadata.basket
            save_info = intent.metadata.save_info
            billing_details = intent.charges.data[0].billing_details
            shipping_details = intent.shipping
            grand_total = round(intent.charges.data[0].amount / 100, 2)

            # Set empty strings to null
            for field, value in shipping_details.address.items():
                if value == "":
                    shipping_details.address[field] = None

            # Update profile information if save_info was checked
            profile = None
            username = intent.metadata.username
            if username != 'AnonymousUser':
                profile = UserProfile.objects.get(user__username=username)
                if save_info:
                    profile.default_phone_number = shipping_details.phone
                    profile.default_street_address1 = shipping_details.address.line1
                    profile.default_street_address2 = shipping_details.address.line2
                    profile.default_town_or_city = shipping_details.address.city
                    profile.default_county = shipping_details.address.state
                    profile.default_country = shipping_details.address.country
                    profile.default_postcode = shipping_details.address.postal_code
                    profile.save()

            order_exists = False
            attempt = 1
            while attempt <= 5:
                try:
                    order = Order.objects.get(
                        full_name__iexact=shipping_details.name,
                        email__iexact=billing_details.email,
                        phone_number__iexact=shipping_details.phone,
                        street_address1__iexact=shipping_details.address.line1,
                        street_address2__iexact=shipping_details.address.line2,
                        town_or_city__iexact=shipping_details.address.city,
                        county__iexact=shipping_details.address.state,
                        country__iexact=shipping_details.address.country,
                        postcode__iexact=shipping_details.address.postal_code,
                        grand_total=grand_total,
                        original_basket=basket,
                        stripe_pid=pid,
                    )
                    order_exists = True
                    break
                except Order.DoesNotExist:
                    attempt += 1
                    time.sleep(1)
            if order_exists:
                self._send_confirmation_email(order)
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: \
                        Verified order already in database',
                    status=200)
            else:
                order = None
                try:
                    order = Order.objects.create(
                        full_name=shipping_details.name,
                        user_profile=profile,
                        email=billing_details.email,
                        phone_number=shipping_details.phone,
                        street_address1=shipping_details.address.line1,
                        street_address2=shipping_details.address.line2,
                        town_or_city=shipping_details.address.city,
                        county=shipping_details.address.state,
                        country=shipping_details.address.country,
                        postcode=shipping_details.address.postal_code,
                        original_basket=basket,
                        stripe_pid=pid,
                    )

                    for item_id, item_data in json.loads(basket).items():
                        product = get_object_or_404(Product, id=item_id)

                        order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=item_data,
                            )
                        order_line_item.save()

                        if not product.inventory_updated:
                            product.remove_items_from_inventory(
                                count=item_data, save=True)
   
                except Exception as e:
                    if order:
                        order.delete()
                    return HttpResponse(
                        content=f'Webhook received: {event["type"]} \
                            | ERROR: {e}',
                        status=500)

                self._send_confirmation_email(order)
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: \
                        Created order in webhook',
                    status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

