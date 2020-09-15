from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Product, Category
from .forms import ProductForm, CategoryForm

# Create your views here.

def products(request):
    """ Products page view """
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    context = {
        'products': products,
    }
    return render(request, 'products/base.html', context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect(reverse('add_category'))
        else:
            return redirect(reverse('add_product'))
    else:
        productForm = ProductForm()
    template = 'products/add_product.html'
    context = {
        'productForm': productForm,
    }
    return render(request, template, context)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            return redirect(reverse('add_product'))
        else:
            return redirect(reverse('add_category'))
    else:
        categoryForm = CategoryForm()
    template = 'products/add_category.html'
    context = {
        'categoryForm': categoryForm,
    }
    return render(request, template, context)
    
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