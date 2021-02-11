from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.db.models import Q

from products.models import Product
from recipes.models import Recipe


def search(request):
    """ 
    A view to return product and recipe search requests
    """
    products = Product.objects.all()
    recipes = Recipe.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "Hmm, you don't appear to have entered any search criteria. Please try again.")
                return redirect('products')

        product_queries = Q(
            name__icontains=query) | Q(description__icontains=query)
        recipe_queries = Q(title__icontains=query)
        products = products.filter(product_queries)
        recipes = recipes.filter(recipe_queries)

    context = {
        'search_term': query,
        'products': products,
        'recipes': recipes,
        }

    return render(request, 'search/search_results.html', context)
