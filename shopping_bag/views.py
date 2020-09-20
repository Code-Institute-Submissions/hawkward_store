from django.shortcuts import render

# Create your views here.

def shopping_bag(request):
    return render(request, 'shopping_bag/base.html')