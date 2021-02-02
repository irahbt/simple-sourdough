from django.shortcuts import render

def checkout_plan(request):
    return render(request, 'checkout_plan/checkout_plan.html')

