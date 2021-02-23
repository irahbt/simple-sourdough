from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """

    Retrieve all products and filter by category
    Retrieve sorting information and direction

    Returns:
    Products page with ability to filter by category and sort products

    """

    products = Product.objects.all()
    category = None
    sort = None
    direction = None

    if request.GET:
        if 'category' in request.GET:
            category = request.GET['category'].split(',')
            products = products.filter(category__name__in=category)
            category = Category.objects.filter(name__in=category)

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'current_category': category,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """

    Retrieve individual product

    Returns:
    Product detail page of specifified product

    """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """

    Check that user is supseruser
    Save information from product form
    Redirect back to add product page

    Returns:
    Add product page with product form

    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you must be a store owner to do that.')
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Added Successful')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Add Product Failed. \
                Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """

    Check user is superuser
    Retrieve specified product
    Save information from product form
    Redirect back to specified product

    Returns:
    Edit product page with specified product and product form

    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you must be a store owner to do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Update Successful')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Update Product Failed. \
                Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """

    Check user is superuser
    Retrieve specified product
    Delete Product

    Returns:
    Products page

    """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you must be a store owner to do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product Deleted')

    return redirect(reverse('products'))
