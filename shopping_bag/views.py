from django.shortcuts import render, redirect, get_object_or_404
from products.models import ProductsStore

# Create your views here.

def shopping_bag(request):
    return render(request, 'shopping_bag/base.html')

def add_item_to_bag(request, product_id):
    product = get_object_or_404(ProductsStore, pk=product_id)
    quantity = 1
    shopping_bag = request.session.get('shopping_bag', {})

    if request.POST:        
        shopping_bag = request.session.get('shopping_bag', {})
        quantity = int(request.POST['quantity'])
        if product_id in list(shopping_bag.keys()):
            shopping_bag[product_id] += quantity
        else:
            shopping_bag[product_id] = quantity        
        request.session['shopping_bag'] = shopping_bag
        return redirect('shopping_bag')
        
    if product_id in list(shopping_bag.keys()):
        shopping_bag[product_id] += quantity
    else:
        shopping_bag[product_id] = quantity
    
    request.session['shopping_bag'] = shopping_bag
    return redirect('shopping_bag')

def delete_item_from_bag(request, product_id):
    shopping_bag = request.session['shopping_bag']
    shopping_bag.pop(product_id)
    
    request.session['shopping_bag'] = shopping_bag
    return redirect('shopping_bag')

def change_quantity(request, product_id):
    shopping_bag = request.session['shopping_bag']
    quantity = int(request.POST.get('quantity'))
    shopping_bag[product_id] = quantity
    
    request.session['shopping_bag'] = shopping_bag
    return redirect('shopping_bag')
