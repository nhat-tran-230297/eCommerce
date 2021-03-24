from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .basket import Basket
from store.models import Product

# Create your views here.
def basket_summary(request):
    print(request.session.items())
    return render(request, 'store/basket/summary.html')


def basket_add(request):
    basket = Basket(request)
    
    if request.POST.get('action') == 'post':
        
        product_id = int(request.POST.get('productID'))
        product_quantity = int(request.POST.get('productQuantity'))

        product = get_object_or_404(Product, pk=product_id)
        basket.add(product=product, product_quantity=product_quantity)

        response = JsonResponse({
            'quantity': len(basket)
        })

        return response

    return JsonResponse({
            'test': 'failed'
        })