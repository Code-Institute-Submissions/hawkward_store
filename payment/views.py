from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib.auth.models import User

from users.models import Giftcards, UserProfile
from products.models import ProductsStore
from .models import Order, OrderItems
from django.db.models import Q
from django.db import transaction
from shopping_bag.contexts import shopping_bag_items

from users.forms import GiftcardsForm, UserProfileForm
from payment.forms import OrderForm

import stripe
import json


# Create your views here.


def check_for_free_items(request):
    shopping_bag = request.session['shopping_bag']
    counter = 0
    for product_id, quantity in shopping_bag.items():
        product = get_object_or_404(ProductsStore, pk=product_id)
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
        form = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'country': request.POST['country'],
            'street_address': request.POST['street_address'],
            'city': request.POST['city'],
            'postcode': request.POST['postcode'],
            'phone_number': request.POST['phone_number'],
        }

        order_form = OrderForm(form)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.total = int(request.session['total'])
            order.all_products = json.dumps(shopping_bag)
            order.free_products = json.dumps(free_items)
            if request.user.is_authenticated:
                user = User.objects.get(username=request.user)
                order.user_profile = user
            order.save()
            for product_id, quantity in shopping_bag.items():
                product = ProductsStore.objects.get(pk=product_id)
                order_item = OrderItems(
                    order=order,
                    product=product,
                    quantity=quantity,
                )
                order_item.save()
            if 'save_info' in request.POST:
                if request.user.is_authenticated:
                    user = User.objects.get(username=request.user)
                    user_form = {
                        'first_name': order.first_name,
                        'last_name': order.last_name,
                        'email': order.email,
                        'country': order.country,
                        'street_address': order.street_address,
                        'city': order.city,
                        'postcode': order.postcode,
                        'phone_number': order.phone_number,
                    }
                    create_user_profile = UserProfileForm(user_form)
                    if create_user_profile.is_valid():
                        create_user_profile.save()
            if 'shopping_bag' in request.session:
                del request.session['shopping_bag']
            if 'free_items' in request.session:
                del request.session['free_items']
            del request.session['total']
            return redirect('payment_success')
        else:
            ''' reset giftcard to old state '''
            for product_id, quantity in shopping_bag.items():
                product = get_object_or_404(ProductsStore, pk=product_id)
                if product.has_giftcard == True:
                    giftcard_q_delete = Giftcards.objects.filter(
                        Q(product_id=product_id) & Q(user=request.user))
                    if giftcard_q_delete:
                        giftcard_q_delete = Giftcards.objects.filter(
                            Q(product_id=product_id) & Q(user=request.user))[0]
                        old_counter = int(giftcard_q.counter + quantity)
                        while old_counter >= 7:
                            old_counter = int(giftcard_q.counter - 7)
                        giftcard_q_delete.counter = old_counter
                        giftcard_q_delete.save()
                    del request.session['free_items']

            return redirect(reverse('products'))

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
            product = get_object_or_404(ProductsStore, pk=product_id)
            total_saved += int(product.price * quantity)
            product_saved.append({
                f'{product_id}': quantity,
            })
    total = int(total_price - total_saved)
    request.session['total'] = total
    if total < 0:
        del request.session['free_items']
        del request.session['total']
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


@login_required
def subscription(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    context = {
        'stripe_public_key': stripe_public_key,
    }
    return render(request, 'payment/subscription.html', context)


@require_POST
@login_required
def subscription_payment_method(request):
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    plan1 = settings.STRIPE_PLAN_MONTHLY_ID
    plan2 = settings.STRIPE_PLAN_YEARLY_ID
    stripe.api_key = stripe_secret_key
    currency = settings.STRIPE_CURRENCY
    payment_method = 'card'
    customer_email = request.user.email
    amount = 0
    plan = ''

    if request.POST['subscription_plan'] == 'plan1':
        plan = plan1
        amount = 1000
    elif request.POST['subscription_plan'] == 'plan2':
        plan = plan2
        amount = 10000
    stripe_plan_id = plan

    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        payment_method_types=['card'],
    )
    secret_key = payment_intent.client_secret
    payment_intent_id = payment_intent.id
    context = {
        'secret_key': secret_key,
        'stripe_public_key': stripe_public_key,
        'customer_email': customer_email,
        'payment_intent_id': payment_intent_id,
        'stripe_plan_id': stripe_plan_id,
    }

    return render(request, 'payment/subscription_intent.html', context)


@require_POST
@login_required
def subscription_backend(request):
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    stripe.api_key = stripe_secret_key
    payment_intent_id = request.POST['payment_intent_id']
    payment_method_id = request.POST['payment_method_id']
    stripe_plan_id = request.POST['stripe_plan_id']
    customer = stripe.Customer.create(
        email=request.user.email,
        payment_method_id=payment_method_id,
        invoice_settings={
            'default_payment_method': payment_method_id
        }
    )
    stripe.Subscription.create(
        customer=customer.id,
        items=[
            {
                'plan': stripe_plan_id
            },
        ]
    )
    stripe.PaymentIntent.modify(
        payment_intent_id,
        payment_method=payment_method_id,
        customer=customer.id
    )
    stripe.PaymentIntent.confirm(
        payment_intent_id
    )
    return render(request, 'payment/subscription_success.html')
