from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Product, Category, Animals
from .forms import ProductForm, CategoryForm, AnimalsForm

# Create your views here.


def products(request):
    """ Products page view """
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/base.html', context)


def product_information(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def product_management(request):
    template = 'products/product_management.html'
    context = {
        'ProductForm': ProductForm,
        'CategoryForm': CategoryForm,
        'AnimalsForm': AnimalsForm,
    }
    return render(request, template, context)


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return redirect('product_management')


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return redirect('product_management')


@login_required
def add_animal(request):
    if request.method == 'POST':
        form = AnimalsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return redirect('product_management')


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
        else:
            return redirect('add_product')
    else:
        form = ProductForm(instance=product)

    template = 'products/edit_product.html'
    context = {
        'productForm': form,
        'product': product,
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return redirect('products')