from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from profiles.models import UserProfile


def recipes(request):
    """ A view to return the recipes page """
    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=request.user)
        recipes = Recipe.objects
        template = 'recipes/recipes.html'
        context = {
            'profile': profile,
            'recipes': recipes,
        }
        return render(request, template, context)
 
    return render(request, 'recipes/recipes.html')


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
        except UserProfile.DoesNotExist:
            return redirect('account_signup')
    return redirect('account_login')
    template = 'recipes/recipe.html'
    context = {
        'recipe': recipe,
    }
    return render(request, template, context)
