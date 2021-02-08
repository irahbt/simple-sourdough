from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from profiles.models import UserProfile

import stripe


def subscriptions(request):
    """ A view to return the subscriptions page """

    return render(request, 'subscriptions/subscriptions.html')


@login_required
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)