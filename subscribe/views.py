from django.shortcuts import render


def subscribe(request):
    """ A view to return the subscribe page """

    return render(request, 'subscribe/subscribe.html')