from django.shortcuts import render

from products.models import Product
from recipes.models import Recipe


def index(request):
    """ A view to return the index page """
    featured_products = Product.objects.filter(featured=True)
    featured_recipes = Recipe.objects.filter(featured=True)


    context = {
        'featured_products': featured_products,
        'featured_recipes': featured_recipes,
    }

    return render(request, 'home/index.html', context)



