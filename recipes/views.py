from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from profiles.models import UserProfile

import stripe


def recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.premium:
        if request.user.is_authenticated:
            try:
                if request.user.userprofile.membership:
                    return render(request, 'recipes/recipe.html', {'recipe': recipe})
            except UserProfile.DoesNotExist:
                return redirect('account_signup')
        return redirect('account_login')
    else:
        context = {
            'recipe': recipe,
        }
        return render(request, 'recipes/recipe.html', context)
