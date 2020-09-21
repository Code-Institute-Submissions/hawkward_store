from django.shortcuts import render, get_object_or_404
from products.models import Product

# Create your views here.

def shopping_bag(request):
    context = {
        'shopping_bag': request.session['shopping_bag']
    }
    return render(request, 'shopping_bag/base.html', context)

def add_item_to_bag(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    

    return render(request, 'shopping_bag/base.html', context)
