from django.http.response import JsonResponse
from django.shortcuts import render

from basket.basket import Basket

from .models import Order, OrderItem


# Create your views here.
def add(request):
    basket = Basket(request)

    if request.POST.get('action') == 'post':
        user_id = request.user.id
        basket_price = basket.get_basket_price
        order_key = request.POST['order_key']
        print(order_key)

        # Check if order (by order_key) exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user_id=user_id, 
                order_key=order_key,
                full_name=request.POST['fullname'],
                address1=request.POST['address1'],
                address2=request.POST['address2'],
                city=request.POST['city'],
                country=request.POST['country'],
                post_code=request.POST['postcode'],
                total_price=basket_price,
            )

            for item in basket:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['total_price'],
                    quantity=item['qty']
                )

        return JsonResponse({'status': 'success'})
    