from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings

from users.models import Giftcards, UserProfile
from products.models import Product
from django.db.models import Q
from shopping_bag.contexts import shopping_bag_items

from users.forms import GiftcardsForm
from payment.forms import OrderForm

import stripe
import json


# Create your views here.


def check_for_free_items(request):
    shopping_bag = request.session['shopping_bag']
    counter = 0
    for product_id, quantity in shopping_bag.items():
        product = get_object_or_404(Product, pk=product_id)
        if product.has_giftcard == True:
            giftcard_q = Giftcards.objects.filter(
                Q(product_id=product_id) & Q(user=request.user))
            if giftcard_q:
                giftcard_q = Giftcards.objects.filter(
                    Q(product_id=product_id) & Q(user=request.user))[0]
                counter = int(giftcard_q.counter + quantity)
                giftcard_q.counter = counter
                if giftcard_q.counter >= 7:
                    free_items = request.session.get('free_items', {})
                    if not free_items:
                        free_items[f'{product_id}'] = 1
                    else:
                        free_items[f'{product_id}'] += 1
                    new_counter = int(giftcard_q.counter - 7)
                    giftcard_q.counter = new_counter
                    while giftcard_q.counter >= 7:
                        new_counter = int(giftcard_q.counter - 7)
                        giftcard_q.counter = new_counter
                        free_items[f'{product_id}'] += 1
                        request.session['free_items'] = free_items
                    request.session['free_items'] = free_items
                giftcard_q.save()
            else:
                user = request.user
                product_id = product_id
                product_name = product.name
                counter = int(quantity)
                giftcard_q = Giftcards(
                    user=user, product_id=product_id, product_name=product_name, counter=counter)
                giftcard_q.save()
    return redirect('payment_processing')


def payment_processing(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':        
        shopping_bag = request.session.get('shopping_bag', {})
        free_items = request.session.get('free_items', {})


    shopping_bag = request.session.get('shopping_bag', {})
    free_items = request.session.get('free_items', {})
    if not shopping_bag:
        return redirect(reverse('products'))
    all_products = shopping_bag_items(request)
    total_price = all_products['total_price']
    total_saved = 0
    product_saved = []
    if free_items:
        for product_id, quantity in free_items.items():
            product = get_object_or_404(Product, pk=product_id)
            total_saved += int(product.price * quantity)
            product_saved.append({
                f'{product_id}': quantity,
            })
    total = int(total_price - total_saved)
    if total < 0:
        del request.session['free_items']
        return redirect('products')
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    order_form = OrderForm()
    context = {
        'total': total,
        'product_saved': product_saved,
        'total_saved': total_saved,
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, 'payment/payment.html', context)

def payment_success(request):
    return render(request, 'payment/payment_success.html')