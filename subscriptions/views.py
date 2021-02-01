from django.shortcuts import render, redirect, reverse, get_object_or_404

from .models import SubscriptionPlan


def subscriptions(request):
    """ Display the subscription page  """
    plans = SubscriptionPlan.objects.all()
    context = {
        'plans': plans,
    }

    return render(
        request, 'subscriptions/subscriptions.html', context)


def plan(request, pk):
    plan = get_object_or_404(SubscriptionPlan, pk=pk)
    if plan.premium:
        return redirect('account_login')
    else:
        return render(request, 'subscriptions/subscriptions.html', {'plan': plan})