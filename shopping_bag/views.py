from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product

# Create your views here.

def shopping_bag(request):
    print(request.session['shopping_bag'])
    return render(request, 'shopping_bag/base.html')

def add_item_to_bag(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = 1
    shopping_bag = request.session.get('shopping_bag', {})

    if request.POST:
        quantity = int(request.POST['quantity'])
        if product_id in list(shopping_bag.keys()):
            shopping_bag[product_id] += quantity
        else:
            shopping_bag[product_id] = quantity

    if product_id in list(shopping_bag.keys()):
        shopping_bag[product_id] += quantity
    else:
        shopping_bag[product_id] = quantity
    
    request.session['shopping_bag'] = shopping_bag
    print(request.session['shopping_bag'])
    return redirect('shopping_bag')
