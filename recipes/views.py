from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Recipe
from profiles.models import UserProfile


def recipes(request):
    """ A view to return the recipes page """
    recipes = Recipe.objects.all()
    template = 'recipes/recipes.html'
    context = {
        'recipes': recipes,
    }
 
    return render(request, template, context)


def recipe(request, pk):
    """
    A view to return an individual recipe page,
    ensuring user has a membership to view
    """
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.user.is_authenticated:
        try:
            if request.user.userprofile.membership:
                template = 'recipes/recipe.html'
                context = {
                    'recipe': recipe
                }
                return render(request, template, context)
            else:
                messages.success(
                    request, 'You need a membership to access recipes. Please subscribe :)')
                return redirect('subscriptions')
        except UserProfile.DoesNotExist:
            messages.success(
                request, 'You need a membership to access recipes. Please login to your account or subscribe now.:)')
            return redirect('account_signup')
    messages.success(
        request, 'You need a membership to access recipes. Please login to your account or subscribe now.:)')
    return redirect('account_login')
    template = 'recipes/recipe.html'
    context = {
        'recipe': recipe,
    }
    return render(request, template, context)
