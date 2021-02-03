from django.shortcuts import render, redirect, get_object_or_404
from .models import RecipePlan
from checkout_plans.models import PlanCustomer
from profiles.models import UserProfile

def subscribe(request):
    plans = RecipePlan.objects
    context = {
            'plans': plans,
        }
    return render(request, 'plans/subscribe.html', context)


def plan(request, pk):
    plan = get_object_or_404(RecipePlan, pk=pk)
    if plan.premium:
        if request.user.is_authenticated:
            try:
                if request.user.userprofile.membership:
                    return render(request, 'plans/plan.html', {'plan': plan})
            except PlanCustomer.DoesNotExist:
                return redirect('subscribe')
        return redirect('account_login')
    else:
        context = {
            'plan': plan,
        }
        return render(request, 'plans/plan.html', context)


