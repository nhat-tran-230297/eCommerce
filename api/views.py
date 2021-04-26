
from django.shortcuts import render
from rest_framework import filters, generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response


from store.models import Category, Product
from basket.basket import Basket

from .serializers import (
    CategorySerializer, 
    ProductCreateSerializer,
    ProductSerializer,
    BasketAddSerializer,
    BasketRemoveSerializer,
    BasketUpdateSerializer
)


# Create your views here.
class APIProductListView(generics.ListAPIView):
    """
    Product List
    """

    queryset = Product.active_products.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = PageNumberPagination

    # search filter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', '=product_code']
    ordering_fields = ['title', 'product_code', 'price']


class APIProductCreateView(generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


class APIProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.active_products.all()
    serializer_class = ProductCreateSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticated, IsAdminUser)


class APICategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = PageNumberPagination
    

class APIBasketView(generics.ListAPIView):
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        basket = Basket(request)

        response = {
            'total_qty': basket.get_basket_qty,
            'total_price': basket.get_basket_price,
            'items_list': {}
        }
        for pk, item_detail in basket.basket.items():
            title = item_detail['title']
            response['items_list'][title] = item_detail
            

        return Response(response)


class APIBasketAddView(generics.CreateAPIView):
    serializer_class = BasketAddSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            basket = Basket(request)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            product_id = int(request.POST['product_id'])
            qty = int(request.POST['qty'])
            
            try:
                product = Product.active_products.get(pk=product_id)
            except Product.DoesNotExist:
                return Response({
                    'product_id': f'Product with id {product_id} does not exist'
                })

            basket.add(product=product, product_qty=qty)

            response = {
                'status': f'Product \'{product.title}\' added',
                'total_qty': basket.get_basket_qty,
                'total_price': basket.get_basket_price,
            }

            return Response(response)


class APIBasketRemoveView(generics.CreateAPIView):
    serializer_class = BasketRemoveSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            basket = Basket(request)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            product_id = int(request.POST['product_id'])

            try:
                product = Product.active_products.get(pk=product_id)
            except Product.DoesNotExist:
                return Response({
                    'product_id': f'Product with id {product_id} does not exist'
                })

            if str(product_id) not in basket.basket:
                return Response({
                    "product_id": "This product is not in the basket"
                })

            basket.delete(product=product)

            response = {
                'status': f'Product \'{product.title}\' removed',
                'total_qty': basket.get_basket_qty,
                'total_price': basket.get_basket_price,
            }

            return Response(response)


class APIBasketUpdateView(generics.UpdateAPIView):
    serializer_class = BasketUpdateSerializer
    permission_classes = (AllowAny, )

    def put(self, request, *args, **kwargs):
        if request.method == 'PUT':
            basket = Basket(request)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            product_id = int(request.POST['product_id'])
            qty = int(request.POST['qty'])
            
            try:
                product = Product.active_products.get(pk=product_id)
            except Product.DoesNotExist:
                return Response({
                    'product_id': f'Product with id {product_id} does not exist'
                })

            if str(product_id) not in basket.basket:
                return Response({
                    "product_id": "This product is not in the basket"
                })

            basket.update(product=product, product_qty=qty)

            response = {
                'status': f'Product \'{product.title}\' updated',
                'total_qty': basket.get_basket_qty,
                'total_price': basket.get_basket_price,
            }

            return Response(response)


