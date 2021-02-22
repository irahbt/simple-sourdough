from django.shortcuts import render

from products.models import Product
from recipes.models import Recipe


def index(request):
    """

    Filters products and recipes by featured = True

    Returns:
    Index page with featured products and recipes

    """
    featured_products = Product.objects.filter(featured=True)
    featured_recipes = Recipe.objects.filter(featured=True)

    context = {
        'featured_products': featured_products,
        'featured_recipes': featured_recipes,
    }

    return render(request, 'home/index.html', context)
