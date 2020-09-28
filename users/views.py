from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Giftcards, UserSubscriptions, UserProfile
from payment.models import Order, OrderItems

# Create your views here.

@login_required
def users(request):
    context = {}
    userprofile = UserProfile.objects.filter(user=request.user)
    if userprofile:
        context['userprofile'] = userprofile
    subscription = UserSubscriptions.objects.filter(user=request.user.username)
    if subscription:        
        context['subscription'] = UserSubscriptions.objects.filter(user=request.user.username)[0]
    giftcards = Giftcards.objects.filter(user=request.user)
    orders = Order.objects.filter(user_profile=request.user)

    context['giftcards'] = giftcards
    context['orders'] = orders
    return render(request, 'users/base.html', context)
