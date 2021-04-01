from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Product

from .basket import Basket


# Create your views here.
def basket_summary(request):
    print(request.session.items())
    return render(request, 'basket/summary.html')


def basket_add(request):
    basket = Basket(request)
    
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productID'))
        product_qty = int(request.POST.get('productQty'))

        product = get_object_or_404(Product, pk=product_id)
        basket.add(product=product, product_qty=product_qty)

        return JsonResponse({
            'basket_qty': basket.get_basket_qty,
            'basket_price': basket.get_basket_price,
            'item_total_price': basket.basket[str(product_id)]['total_price'],
        })

    return JsonResponse({'success': 'failed'})


def basket_delete(request):
    basket = Basket(request)

    if request.POST.get('action') == 'delete':
        
        product_id = int(request.POST.get('productID'))

        product = get_object_or_404(Product, pk=product_id)
        basket.delete(product=product)

        return JsonResponse({
            'basket_qty': basket.get_basket_qty,
            'basket_price': basket.get_basket_price,
        })

    return JsonResponse({'success': 'failed'})


# def basket_add(request):
#     basket = Basket(request)
    
#     if request.POST.get('action') == 'post':
        
#         product_id = int(request.POST.get('productID'))
#         product_qty = int(request.POST.get('productQty'))

#         product = get_object_or_404(Product, pk=product_id)
#         basket.add(product=product, product_qty=product_qty)

#         return JsonResponse({
#             'basket_qty': basket.get_basket_qty,
#         })

#     return JsonResponse({'success': 'failed'})