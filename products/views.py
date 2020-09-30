from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from .models import ProductsStore, Category, Animals
from .forms import ProductsStoreForm, CategoryForm, AnimalsForm

# Create your views here.


def products(request):
    """ Products page view """
    products = ProductsStore.objects.all().order_by('name')
    active = None
    query = None
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query) | Q(
                    category__name__icontains=query) | Q(
                        animal__name__icontains=query)
            products = products.filter(queries)
        if 'all' in request.GET:
            active = 'all'
            products = ProductsStore.objects.all().order_by('name')
        if 'new' in request.GET:
            active = 'new'
            products = ProductsStore.objects.order_by('-pk')
        if 'dog_food' in request.GET:
            active = 'dog_food'
            products = ProductsStore.objects.filter(
                Q(animal__name__icontains='dog') & Q(category__name__icontains='food'))
        if 'dog_toys' in request.GET:
            active = 'dog_toys'
            products = ProductsStore.objects.filter(
                Q(animal__name__icontains='dog') & Q(category__name__icontains='toys'))
        if 'dog_other' in request.GET:
            active = 'dog_other'
            products = ProductsStore.objects.filter(Q(animal__name__icontains='dog')).exclude(
                Q(category__name__icontains='food')).exclude(Q(category__name__icontains='toys'))
        if 'cat_food' in request.GET:
            active = 'cat_food'
            products = ProductsStore.objects.filter(
                Q(animal__name__icontains='cat') & Q(category__name__icontains='food'))
        if 'cat_toys' in request.GET:
            active = 'cat_toys'
            products = ProductsStore.objects.filter(
                Q(animal__name__icontains='cat') & Q(category__name__icontains='toys'))
        if 'cat_other' in request.GET:
            active = 'cat_other'
            products = ProductsStore.objects.filter(Q(animal__name__icontains='cat')).exclude(
                Q(category__name__icontains='food')).exclude(Q(category__name__icontains='toys'))
        if 'giftcard' in request.GET:
            active = 'giftcard'
            products = ProductsStore.objects.filter(has_giftcard=True)
        if 'other' in request.GET:
            active = 'other'
            products = ProductsStore.objects.all().exclude(
                Q(category__name__icontains='food')).exclude(
                    Q(category__name__icontains='toys')).exclude(
                        Q(animal__name__icontains='cat')).exclude(
                            Q(animal__name__icontains='dog'))

    context = {
        'products': products,
        'active': active,
    }

    return render(request, 'products/base.html', context)


def product_information(request, product_id):
    """ Products information view """
    product = get_object_or_404(ProductsStore, pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def product_management(request):
    """ Products management view """
    template = 'products/product_management.html'
    context = {
        'ProductForm': ProductsStoreForm,
        'CategoryForm': CategoryForm,
        'AnimalsForm': AnimalsForm,
    }
    return render(request, template, context)


@login_required
def add_product(request):
    """ Adding a product view """
    if request.method == 'POST':
        form = ProductsStoreForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return redirect('product_management')


@login_required
def add_category(request):
    """ Adding a category view """
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return redirect('product_management')


@login_required
def add_animal(request):
    """ Adding a animal view """
    if request.method == 'POST':
        form = AnimalsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return redirect('product_management')


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """

    product = get_object_or_404(ProductsStore, pk=product_id)
    if request.method == 'POST':
        form = ProductsStoreForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
        else:
            return redirect('add_product')
    else:
        form = ProductsStoreForm(instance=product)

    template = 'products/edit_product.html'
    context = {
        'productForm': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Deleting a Product from the Store """
    product = get_object_or_404(ProductsStore, pk=product_id)
    product.delete()
    return redirect('products')
