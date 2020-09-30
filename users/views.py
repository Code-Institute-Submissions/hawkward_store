from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .forms import UserProfileForm
from .models import Giftcards, UserSubscriptions, UserProfile
from products.models import ProductsStore
from payment.models import Order, OrderItems

# Create your views here.


@login_required
def users(request):
    context = {}
    product = ProductsStore.objects.latest('pk')
    try:
        userprofile = UserProfile.objects.get(user=request.user)
        user_form = UserProfileForm(initial={
            'first_name': userprofile.first_name,
            'last_name': userprofile.last_name,
            'email': userprofile.email,
            'country': userprofile.country,
            'street_address': userprofile.street_address,
            'city': userprofile.city,
            'postcode': userprofile.postcode,
            'phone_number': userprofile.phone_number,
        })
    except UserProfile.DoesNotExist:
        user_form = UserProfileForm()
    subscription = UserSubscriptions.objects.filter(user=request.user.username)
    if subscription:
        context['subscription'] = UserSubscriptions.objects.filter(
            user=request.user.username)[0]
    giftcards = Giftcards.objects.filter(user=request.user)
    orders = Order.objects.filter(user_profile=request.user)
    if 'success' in request.session:
        context['success'] = request.session['success']
        del request.session['success']
    context['user_form'] = user_form
    context['giftcards'] = giftcards
    context['orders'] = orders
    context['product'] = product
    return render(request, 'users/base.html', context)


@login_required
def update_or_create_user(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user_profile = UserProfile.objects.filter(user=user)
        success = ""
        if user_profile:
            user_profile = UserProfile.objects.filter(user=user)[0]
            user_profile.first_name = request.POST['first_name']
            user_profile.last_name = request.POST['last_name']
            user_profile.email = request.POST['email']
            user_profile.country = request.POST['country']
            user_profile.street_address = request.POST['street_address']
            user_profile.city = request.POST['city']
            user_profile.postcode = request.POST['postcode']
            user_profile.phone_number = request.POST['phone_number']
            user_profile.save()
            success = "You have successfully updated your Profile!"
            request.session['success'] = success
        else:
            create_user_profile = UserProfile(
                user=user, first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                email=request.POST['email'], country=request.POST['country'], street_address=request.POST['street_address'],
                city=request.POST['city'], postcode=request.POST['postcode'], phone_number=request.POST['phone_number'],
            )
            create_user_profile.save()
            success = "You have successfully created your Profile!"
            request.session['success'] = success
    return redirect('users')
