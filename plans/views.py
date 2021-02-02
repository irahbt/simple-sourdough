from django.shortcuts import render, redirect, get_object_or_404
from .models import RecipePlan


def subscribe(request):
    return render(request, 'plans/subscribe.html')


def plan(request, pk):
    plan = get_object_or_404(RecipePlan, pk=pk)
    if plan.premium:
        return redirect('subscribe')
    else:
        context = {
            'plan': plan,
        }
        return render(request, 'plans/plan.html', context)


def checkout_for_plan(request):
    return render(request, 'plans/checkout_plan.html')