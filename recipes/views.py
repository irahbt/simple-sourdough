from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms


from .models import Recipe, Ingredient
from .forms import IngredientForm, RecipeForm

from profiles.models import UserProfile


def recipes(request):
    """

    Retrieves all recipes
    Check if user is authenticated and retireve profile

    Returns:
    Recipes page and profile

    """
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

    Retrieve indivual recipe
    Check if recipe is premium
    Check if user is authenticated and if user profile has membership
    Ensure user has membership to view premium recipes

    Returns:
    Specified recipe's page

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
                        request, 'You need a membership to \
                            access premium recipes.')
                    return redirect('subscriptions')
            except UserProfile.DoesNotExist:
                messages.info(
                    request, 'You need a membership to access premium recipes. \
                        Please sign in to your account or subscribe now.')
                return redirect('account_signup')
        messages.info(
            request, 'You need a membership to access premium recipes. \
                Please sign in to your account or subscribe now.')
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

    Check user is supseruser
    Save information from recipe form
    Redirect back to add recipe page
    Retrieve all ingredients

    Returns:
    Add recipe page with product form, ingredient form and all ingredients

    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you must be a store owner to do that.')
        return redirect(reverse('home'))

    IngredientFormSet = forms.inlineformset_factory(
        Recipe, Ingredient, form=IngredientForm, can_delete=True)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        # formset = IngredientFormSet(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save()
            formset = IngredientFormSet(
                request.POST, instance=recipe)

            if formset.is_valid():
                recipe.save
                formset.save()
                messages.success(request, 'Recipe Added Successfuly')
                return redirect('recipes')
            else:
                messages.error(
                    request, 'Add Recipe Failed. \
                        Please ensure the ingredient form is valid')
        else:
            messages.error(
                request, 'Add Recipe Failed. Please ensure the form is valid.')

    else:
        form = RecipeForm()
        formset = IngredientFormSet()

    template = 'recipes/add_recipe.html'
    context = {
        'formset': formset,
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_recipe(request, recipe_id):
    """

    Check user is superuser
    Retrieve specified recipe
    Save information from recipe form
    Redirect back to specified recipe

    Returns:
    Edit recipe page with specified recipe and recipe form

    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you must be a store owner to do that.')
        return redirect(reverse('home'))

    IngredientFormSet = forms.inlineformset_factory(
        Recipe, Ingredient, form=IngredientForm, can_delete=True, extra=0)

    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)

        if form.is_valid():
            recipe = form.save()
            formset = IngredientFormSet(request.POST, instance=recipe)
            if formset.is_valid():
                # recipe.save
                formset.save()
                messages.success(request, 'Recipe Update Successful')
                return redirect(reverse('recipe', args=[recipe.id]))
            else:
                messages.error(
                    request, 'Update Recipe Failed. \
                        Please ensure the ingredient form is valid.')
        else:
            messages.error(
                request, 'Update Recipe Failed. \
                    Please ensure the form is valid.')
    else:
        form = RecipeForm(instance=recipe)
        formset = IngredientFormSet(instance=recipe)
        messages.info(request, f'You are editing {recipe.title}')

    template = 'recipes/edit_recipe.html'
    context = {
        'form': form,
        'formset': formset,
        'recipe': recipe,
    }

    return render(request, template, context)


@login_required
def delete_recipe(request, recipe_id):
    """

    Check user is superuser
    Retrieve specified recipe
    Delete Recipe

    Returns:
    Recipes page

    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you must be a store owner to do that.')
        return redirect(reverse('home'))

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.delete()
    messages.success(request, 'Recipe Deleted')

    return redirect(reverse('recipes'))
