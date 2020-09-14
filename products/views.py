from django.shortcuts import render, redirect, reverse
from django.db.models import Q

from .models import Product, Category
from .forms import ProductForm, CategoryForm

# Create your views here.

def products(request):
    """ Products page view """
    return render(request, 'products/base.html')

def add_product(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
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