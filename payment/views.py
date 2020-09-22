from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings

from users.models import Giftcards, UserProfile
from products.models import Product
from django.db.models import Q

from users.forms import GiftcardsForm
from payment.forms import OrderForm


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

    context = {
        'OrderForm': OrderForm,
    }
    return render(request, 'payment/payment.html', context)

@require_POST
def payment_processing(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.all_products = json.dumps(bag)
            order.save()
    return redirect('shopping_bag')

