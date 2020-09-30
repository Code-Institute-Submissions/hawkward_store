from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from decimal import Decimal
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from users.models import Giftcards, UserProfile, UserSubscriptions
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
    ''' checking the giftcard system and adding free items to the session '''
    if request.user.is_authenticated:
        shopping_bag = request.session['shopping_bag']
        if not shopping_bag:
            return redirect('shopping_bag')
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
    return redirect('payment')


def payment(request):
    ''' rendering the payment, order form, billing information '''
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
    total = Decimal(stripe_total / 100)
    request.session['stripe_total'] = stripe_total
    total = round(total, 2)
    if request.user.is_authenticated:
        try:
            userprofile = UserProfile.objects.get(user=request.user)
            order_form = OrderForm(initial={
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
            order_form = OrderForm()
    else:
        order_form = OrderForm()
    context = {
        'total': total,
        'product_saved': product_saved,
        'total_saved': total_saved,
        'order_form': order_form,
    }
    return render(request, 'payment/payment.html', context)


@require_POST
def payment_method(request):
    ''' taking payment form/billing information, creating an order and creating a stripe intent '''
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    stripe.api_key = stripe_secret_key
    currency = settings.STRIPE_CURRENCY
    amount = request.session['stripe_total']
    if not amount or amount < 0:
        del request.session['stripe_total']
        something = "Something went wrong! Please try Again!"
        context = {
            'something': something
        }
        return render(request, 'payment/wherrors.html', context)
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
        order.total = int(request.session['total'])
        order.all_products = json.dumps(shopping_bag)
        order.free_products = json.dumps(free_items)
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            order.user_profile = user

        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
        )

        order.stripe_pid = payment_intent.id
        order.save()
        for product_id, quantity in shopping_bag.items():
            product = ProductsStore.objects.get(pk=product_id)
            order_item = OrderItems(
                order=order,
                product=product,
                quantity=quantity,
            )
            order_item.save()
        if 'save-info' in request.POST:
            if request.user.is_authenticated:
                user = User.objects.get(username=request.user)
                user_profile = UserProfile.objects.filter(user=user)
                if user_profile:
                    user_profile = UserProfile.objects.filter(user=user)[0]
                    user_profile.first_name = order.first_name
                    user_profile.last_name = order.last_name
                    user_profile.email = order.email
                    user_profile.country = order.country
                    user_profile.street_address = order.street_address
                    user_profile.city = order.city
                    user_profile.postcode = order.postcode
                    user_profile.phone_number = order.phone_number
                    user_profile.save()
                else:
                    create_user_profile = UserProfile(
                        user=user, first_name=order.first_name, last_name=order.last_name,
                        email=order.email, country=order.country, street_address=order.street_address,
                        city=order.city, postcode=order.postcode, phone_number=order.phone_number,
                    )
                    create_user_profile.save()
    customer_email = order.email
    secret_key = payment_intent.client_secret
    payment_intent_id = payment_intent.id
    order_number = order.order_number
    context = {
        'secret_key': secret_key,
        'stripe_public_key': stripe_public_key,
        'customer_email': customer_email,
        'payment_intent_id': payment_intent_id,
        'order_number': order_number,
    }

    return render(request, 'payment/payment_intent.html', context)


@require_POST
def payment_backend(request):
    ''' trying to confirm stripe intent and creating order. redirecting to 3dsecure if needed or going to error page '''
    shopping_bag = request.session.get('shopping_bag', {})
    free_items = request.session.get('free_items', {})
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    stripe.api_key = stripe_secret_key
    if request.POST['payment_method_id']:
        payment_method_id = request.POST['payment_method_id']
    else:
        something = "Something went wrong! Please try Again!"
        context = {
            'something': something
        }
        return render(request, 'payment/wherrors.html', context)
    payment_intent_id = request.POST['payment_intent_id']
    order_number = request.POST['order_number']
    order = Order.objects.filter(order_number=order_number)
    if order:
        order = Order.objects.filter(order_number=order_number)[0]
        try:
            ret = stripe.PaymentIntent.confirm(
                payment_intent_id,
                payment_method=payment_method_id
            )

            if ret.status == 'requires_payment_method':
                order.delete()
                return redirect('shopping_bag')
            if ret.status == 'requires_action':
                pi = stripe.PaymentIntent.retrieve(
                    payment_intent_id
                )
                context = {}

                context['payment_intent_secret'] = pi.client_secret
                context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLIC_KEY
                context['order'] = order.order_number
                context['cust_email'] = request.POST['customer_email']
                return render(request, 'payment/3dsec.html', context)

            cust_email = request.POST['customer_email']
            subject = render_to_string(
                'payment/confirmation_emails/confirmation_email_subject.txt',
                {'order': order})
            body = render_to_string(
                'payment/confirmation_emails/confirmation_email_body.txt',
                {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [cust_email]
            )
            ''' reset giftcard to old state '''
            for product_id, quantity in shopping_bag.items():
                product = get_object_or_404(ProductsStore, pk=product_id)
                if product.has_giftcard == True:
                    giftcard_q_delete = Giftcards.objects.filter(
                        Q(product_id=product_id) & Q(user=request.user))
                    if giftcard_q_delete:
                        giftcard_q_delete = Giftcards.objects.filter(
                            Q(product_id=product_id) & Q(user=request.user))[0]
                        old_counter = int(giftcard_q_delete.counter + quantity)
                        while old_counter >= 7:
                            old_counter = int(giftcard_q_delete.counter - 7)
                        giftcard_q_delete.counter = old_counter
                        giftcard_q_delete.save()

            if 'shopping_bag' in request.session:
                del request.session['shopping_bag']
            if 'free_items' in request.session:
                del request.session['free_items']
            if 'stripe_total' in request.session:
                del request.session['stripe_total']
            if 'total' in request.session:
                del request.session['total']
            success = "Successfully created Order!"
            context = {
                'success': success,
                'order': order,
            }
            return render(request, 'payment/payment_success.html', context)
        except Exception as e:
            if order:
                order.delete()
            something = "Something went wrong! Please try Again!"
            context = {
                'e': e,
                'something': something,
            }
            return render(request, 'payment/wherrors.html', context)
    something = "Something went wrong! Please try Again!"
    context = {
        'something': something
    }
    return render(request, 'payment/wherrors.html', context)


@csrf_exempt
def payment_success(request):
    ''' Payment confirm success saving either subscription or order '''
    if request.method == 'POST':
        subscription = request.POST['subscription']
        if subscription == 'yes':
            success = "You subscribed Successfully!"
            context = {
                'success': success,
            }
            return render(request, 'payment/payment_success.html', context)
        order_number = request.POST['order']
        order = Order.objects.get(order_number=order_number)
        cust_email = request.POST['cust_email']
        subject = render_to_string(
            'payment/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'payment/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )
        if 'shopping_bag' in request.session:
            del request.session['shopping_bag']
        if 'free_items' in request.session:
            del request.session['free_items']
        if 'stripe_total' in request.session:
            del request.session['stripe_total']
        if 'total' in request.session:
            del request.session['total']
        success = "Your order was validated and payment was Confirmed!"
        context = {
            'success': success,
            'order': order,
        }
        return render(request, 'payment/payment_success.html', context)
    something = "Something went wrong! Sorry for the invoncenience!"
    context = {
        'something': something,
    }
    return render(request, 'payment/wherrors.html', context)


@login_required
def subscription(request):
    ''' creating subscription information and letting user choose what plan '''
    user_subscription = UserSubscriptions.objects.filter(
        user=request.user.username)
    if user_subscription:
        user_subscription = UserSubscriptions.objects.filter(
            user=request.user.username)[0]
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    context = {
        'user_subscription': user_subscription,
        'stripe_public_key': stripe_public_key,
    }
    return render(request, 'payment/subscription.html', context)


@require_POST
@login_required
def subscription_payment_method(request):
    ''' creating subscription payment intent with information from previous view '''
    user_subscription = UserSubscriptions.objects.filter(
        user=request.user.username)
    if user_subscription:
        user_subscription = UserSubscriptions.objects.filter(
            user=request.user.username)[0]
        if user_subscription.subscription == True:
            return redirect('users')
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    plan1 = settings.STRIPE_PLAN_MONTHLY_ID
    plan2 = settings.STRIPE_PLAN_YEARLY_ID
    stripe.api_key = stripe_secret_key
    if 'payment_intent_id' in request.session:
        payment_intent_id = request.session['payment_intent_id']
        try:
            stripe.PaymentIntent.cancel(
                payment_intent_id,
            )
            del request.session['payment_intent_id']
        except:
            del request.session['payment_intent_id']
    currency = settings.STRIPE_CURRENCY
    payment_method = 'card'
    customer_email = request.user.email
    amount = 0
    plan = request.POST['subscription_plan']

    if plan == 'plan1':
        plan_id = plan1
        amount = 1000
    elif plan == 'plan2':
        plan_id = plan2
        amount = 10000
    stripe_plan_id = plan_id

    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
    )
    secret_key = payment_intent.client_secret
    payment_intent_id = payment_intent.id
    request.session['payment_intent_id'] = payment_intent_id
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
    ''' confirming subscription intent and either redirecting to 3dsecure, errorpage or succcess page '''
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    stripe.api_key = stripe_secret_key
    payment_intent_id = request.POST['payment_intent_id']
    if request.POST['payment_method_id']:
        payment_method_id = request.POST['payment_method_id']
    else:
        something = "Something went wrong! Please try Again!"
        context = {
            'something': something
        }
        return render(request, 'payment/wherrors.html', context)
    stripe_plan_id = request.POST['stripe_plan_id']
    user_subscription = UserSubscriptions.objects.filter(
        user=request.user.username)
    if not user_subscription:
        new_subscription = UserSubscriptions(
            user=request.user.username, subscription=True)
        try:
            customer = stripe.Customer.create(
                email=request.user.email,
                payment_method=payment_method_id,
                invoice_settings={
                    'default_payment_method': payment_method_id
                }
            )
            s = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {
                        'plan': stripe_plan_id
                    },
                ]
            )
            latest_invoice = stripe.Invoice.retrieve(s.latest_invoice)

            ret = stripe.PaymentIntent.confirm(
                latest_invoice.payment_intent,
            )
            if ret.status == 'succeeded':
                new_subscription.s_id = s.id
                new_subscription.save()
                return render(request, 'payment/subscription_success.html')

            if ret.status == 'requires_payment_method':
                stripe.Customer.delete(customer.id)
                new_subscription.delete()
                return render('subscription')
            if ret.status == 'requires_action':
                new_subscription.s_id = s.id
                new_subscription.save()
                pi = stripe.PaymentIntent.retrieve(
                    latest_invoice.payment_intent
                )

                context = {}

                context['payment_intent_secret'] = pi.client_secret
                context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLIC_KEY
                context['subscription'] = 'yes'
                context['customer_id'] = customer.id

                return render(request, 'payment/3dsec.html', context)
        except Exception as e:
            something = "Something went wrong! Sorry for the invoncenience!"
            context = {
                'e': e,
                'something': something,
            }
            return render(request, 'payment/wherrors.html', context)


@require_POST
@csrf_exempt
def payment_error(request):
    ''' handles all 3dsecure errors '''
    order_number = request.POST['order']
    subscription = request.POST['subscription']
    customer_id = request.POST['customer_id']
    if order_number:
        order = Order.objects.get(order_number=order_number)
        order.delete()
    if subscription == 'yes':
        stripe.Customer.delete(customer.id)
        subscription = UserSubscriptions.objects.get(
            user=request.user.username)
        subscription.delete()
    something = "Something went wrong! Sorry for the invoncenience! Please Try again!"
    context = {
        'something': something,
    }
    return render(request, 'payment/wherrors.html', context)


@login_required
def delete_subscription(request):
    ''' deleting a subscription '''
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    stripe.api_key = stripe_secret_key
    usersubscription = UserSubscriptions.objects.get(
        user=request.user.username)
    if not usersubscription:
        something = "Something went wrong! Sorry for the invoncenience! Please Try again!"
        context = {
            'something': something,
        }
        return render(request, 'payment/wherrors.html', context)
    sub_id = usersubscription.s_id
    if not sub_id:
        usersubscription.delete()
        something = "Subscription Deleted!"
        context = {
            'something': something,
        }
        return render(request, 'payment/wherrors.html', context)
    stripe.Subscription.delete(sub_id)
    usersubscription.delete()
    success = "Successfully deleted Subscription!"
    context = {
        'success': success,
    }
    return render(request, 'payment/payment_success.html', context)
