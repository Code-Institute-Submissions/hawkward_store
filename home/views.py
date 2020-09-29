from django.shortcuts import render
from products.models import ProductsStore

# Create your views here.

def index(request):
    """ Index page view """
    product = ProductsStore.objects.latest('pk')
    context = {
        'product': product
    }
    return render(request, 'home/index.html', context)