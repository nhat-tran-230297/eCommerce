import json

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from basket.basket import Basket
from order.models import Order

# Create your views here.

@login_required
def payment_form(request):
    """
    Payment form
    """

    basket = Basket(request)

    basket_price = str(basket.get_basket_price)
    total = basket_price.replace('.', '')
    total = int(total)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/payment_form.html', {'client_secret': intent.client_secret, 'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY})

@login_required
def payment_complete(request):
    """
    Payment complete view
    """

    basket = Basket(request)
    basket.clear()

    user = request.user
    current_site = get_current_site(request)
    subject = 'Order Placed'
    protocol = 'https' if request.is_secure() else 'http'
    message = render_to_string('payment/payment_complete_email.html', {
        'protocol': protocol,
        'user': user,
        'domain': current_site.domain,
    })

    user.email_user(subject=subject, message=message, email=user.email)

    return render(request, 'payment/payment_complete.html')


@csrf_exempt
def stripe_webhook(request):
    """
    Sent data to webhook
    """

    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), 
            stripe.api_key
        )
        
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        print('payment_intent.succeeded')
        order_key = event.data.object.client_secret
        Order.objects.filter(order_key=order_key).update(billing_status=True)

    elif event.type == 'charge.succeeded':
        print('charge.succeeded')

    else:
        print('Unhandled event type {}'.format(event.type))


    print('Sent to webhook')
    return HttpResponse(status=200)
