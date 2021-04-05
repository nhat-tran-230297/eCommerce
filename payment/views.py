import json
import stripe

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http.response import HttpResponse
from django.conf import settings

from basket.basket import Basket
from .utils import payment_confirmation

# Create your views here.

# @login_required
def payment_detail(request):
    basket = Basket(request)

    basket_price = str(basket.get_basket_price)
    total = basket_price.replace('.', '')
    total = int(total)

    print(total)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/payment_form.html', {'client_secret': intent.client_secret, 'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY})


def payment_complete(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/payment_complete.html')

@csrf_exempt
def stripe_webhook(request):
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
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    print('Sent to webhook')

    return HttpResponse(status=200)