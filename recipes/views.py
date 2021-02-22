from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Recipe, Ingredient
from .forms import IngredientForm, RecipeForm
from profiles.models import UserProfile


def recipes(request):
    """ A view to return the recipes page """
    recipes = Recipe.objects.all()

    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=request.user)
        template = 'recipes/recipes.html'
        context = {
            'recipes': recipes,
            'profile': profile,
            }
        return render(request, template, context)
    else:
        template = 'recipes/recipes.html'
        context = {
            'recipes': recipes,
            }

    return render(request, template, context)


def recipe(request, recipe_id):
    """
    A view to return an individual recipe page,
    ensuring user has a membership to view premium recipes
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if recipe.premium:
        if request.user.is_authenticated:
            try:
                if request.user.userprofile.membership:
                    template = 'recipes/recipe.html'
                    context = {
                        'recipe': recipe
                    }
                    return render(request, template, context)
                else:
                    messages.info(
                        request, 'You need a membership to access premium recipes.')
                    return redirect('subscriptions')
            except UserProfile.DoesNotExist:
                messages.info(
                    request, 'You need a membership to access premium recipes. Please sign in to your account or subscribe now.')
                return redirect('account_signup')
        messages.info(
            request, 'You need a membership to access premium recipes. Please sign in to your account or subscribe now.')
        return redirect('account_login')
    else:
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
            messages.error(
                request, 'Add Recipe Failed. Please ensure the form is valid.')
    else:
        form = RecipeForm()
        ingredient_form = IngredientForm()

    ingredients = Ingredient.objects.all()
    template = 'recipes/add_recipe.html'
    context = {
        'ingredients': ingredients,
        'form': form,
        'ingredient_form': ingredient_form
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
            messages.error(
                request, 'Update Recipe Failed. Please ensure the form is valid.')
    else:
        form = RecipeForm(instance=recipe)
        messages.info(request, f'You are editing {recipe.title}')

    template = 'recipes/edit_recipe.html'
    context = {
        'form': form,
        'recipe': recipe,
    }

    return render(request, template, context)


@login_required
def delete_recipe(request, recipe_id):
    """ Delete a recipe """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you must be a store owner to do that.')
        return redirect(reverse('home'))

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.delete()
    messages.success(request, 'Recipe Deleted')

    return redirect(reverse('recipes'))


@login_required
def add_ingredient(request):
    """
    Add an ingredient
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you must be a store owner to do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = IngredientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingredient Added Successfully')
            return redirect(reverse('add_recipe'))
        else:
            messages.error(
                request, 'Add Ingredient Failed. Please ensure the form is valid.')
            return redirect(reverse('add_recipe'))


@login_required
def edit_ingredient(request, ingredient_id):
    """
    Edit an ingredient
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you must be a store owner to do that.')
        return redirect(reverse('home'))

    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    if request.method == 'POST':
        form = IngredientForm(request.POST, request.FILES, instance=ingredient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingredient Update Successful')
            return redirect('add_recipe')
        else:
            messages.error(
                request, 'Update Ingredient Failed. Please ensure the form is valid.')
    else:
        form = IngredientForm(instance=ingredient)
        messages.info(request, f'You are editing {ingredient.name}')

    template = 'recipes/edit_ingredient.html'
    context = {
        'form': form,
        'ingredient': ingredient,
    }

    return render(request, template, context)


@login_required
def delete_ingredient(request, ingredient_id):
    """ Delete a recipe """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you must be a store owner to do that.')
        return redirect(reverse('home'))

    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    ingredient.delete()
    messages.success(request, 'Ingredient Deleted')

    return redirect(reverse('add_recipe'))

