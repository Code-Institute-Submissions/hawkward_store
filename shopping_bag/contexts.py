from django.conf import settings
from products.models import ProductsStore
from django.shortcuts import get_object_or_404


def shopping_bag_items(request):

    products = []
    total_price = 0
    total_products = 0
    shopping_bag = request.session.get('shopping_bag', {})

    for product_id, quantity in shopping_bag.items():
        product = get_object_or_404(ProductsStore, pk=product_id)
        total_price += quantity * product.price
        total_products += quantity
        products.append({
            'product_id': product_id,
            'quantity': quantity,
            'product': product,
        })

    context = {
        'products': products,
        'total_price': total_price,
        'total_products': total_products,
    }

    return context
