from django.shortcuts import render, get_object_or_404

from .models import SubscriptionPlan


def subscriptions(request):
    """ Display the subscription page . """

    return render(request, 'subscriptions/subscriptions.html')
