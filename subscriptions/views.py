from django.shortcuts import render, redirect, reverse, get_object_or_404

from .models import Subscription


def subscriptions(request):
    """ Display the subscription page  """
    subscriptions = Subscription.objects.all()
    context = {
        'subscriptions': subscriptions
    }

    return render(
        request, 'subscriptions/subscriptions.html', context)



def subscription_detail(request, subscription_id):
    """ A view to show individual subscription details """

    subscription = get_object_or_404(Subscription, pk=subscription_id)

    context = {
        'subscription': subscription,
    }

    return render(request, 'subscriptions/subscription_detail.html', context)
