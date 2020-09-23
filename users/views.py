from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Giftcards

# Create your views here.

@login_required
def users(request):
    giftcards = Giftcards.objects.filter(user=request.user)
    context = {
        'giftcards': giftcards
    }
    return render(request, 'users/base.html', context)
