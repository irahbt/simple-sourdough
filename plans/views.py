from django.shortcuts import render, redirect, get_object_or_404
from .models import RecipePlan
from profiles.models import UserProfile


def subscribe(request):
    return render(request, 'plans/subscribe.html')


def plan(request, pk):
    plan = get_object_or_404(RecipePlan, pk=pk)
    if plan.premium:
        if request.user.is_authenticated:
            try:
                if request.user.userprofile.membership:
                    return render(request, 'plans/plan.html', {'plan': plan})
            except UserProfile.DoesNotExist:
                return redirect('account_signup')
        return redirect('account_login')
    else:
        context = {
            'plan': plan,
        }
        return render(request, 'plans/plan.html', context)
