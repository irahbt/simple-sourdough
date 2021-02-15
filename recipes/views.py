from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Recipe
from .forms import IngredientForm, RecipeForm
from profiles.models import UserProfile


def recipes(request):
    """ A view to return the recipes page """
    recipes = Recipe.objects.all()
    profile = get_object_or_404(UserProfile, user=request.user)

    template = 'recipes/recipes.html'
    context = {
        'profile': profile,
        'recipes': recipes,
    }
 
    return render(request, template, context)


def recipe(request, recipe_id):
    """
    A view to return an individual recipe page,
    ensuring user has a membership to view
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)

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


@login_required
def add_recipe(request):
    """
    Add a recipe
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you must be a store owner to do that.')
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe Added Successful')
            return redirect(reverse('add_recipe'))
        else:
            messages.error(request, 'Add Recipe Failed. Please ensure the form is valid.')
    else:
        form = RecipeForm()

    template = 'recipes/add_recipe.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_recipe(request, recipe_id):
    """
    Edit a recipe
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you must be a store owner to do that.')
        return redirect(reverse('home'))

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe Update Successful')
            return redirect(reverse('recipe', args=[recipe.id]))
        else:
            messages.error(request, 'Update Recipe Failed. Please ensure the form is valid.')
    else:
        form = RecipeForm(instance=recipe)
        messages.info(request, f'You are editing {recipe.title}')

    template = 'recipes/edit_recipe.html'
    context = {
        'form': form,
        'recipe': recipe,
    }

    return render(request, template, context)
