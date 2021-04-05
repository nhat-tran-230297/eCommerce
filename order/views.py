from django.shortcuts import render
from django.http.response import JsonResponse

from basket.basket import Basket
from .models import Order, OrderItem


# Create your views here.
def add(request):
    basket = Basket(request)

    if request.POST.get('action') == 'post':
        user_id = request.user.id
        order_key = request.POST.get('order_key')
        basket_price = basket.get_basket_price

        # Check if order (by order_key) exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user_id=user_id, 
                full_name='Name Name',
                address1='address1',
                address2='address2',
                total_price=basket_price,
                order_key=order_key
            )

            for item in basket:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['total_price'],
                    quantity=item['qty']
                )

        return JsonResponse({'status': 'success'})
    