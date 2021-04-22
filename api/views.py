
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
    queryset = Product.active_products.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = PageNumberPagination

    # authentication_classes = (TokenAuthentication, )

    # search filter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'product_code']
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

            title = request.POST['product_title']
            qty = int(request.POST['qty'])
            product = Product.active_products.filter(title=title).first()

            basket.add(product=product, product_qty=qty)

            response = {
                'status': 'Product added',
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

            title = request.POST['product_title']
            product = Product.active_products.filter(title=title).first()

            basket.delete(product=product)

            response = {
                'status': 'Product removed',
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

            title = request.POST['product_title']
            qty = int(request.POST['qty'])
            product = Product.active_products.filter(title=title).first()

            if not product:
                return Response({
                    "product_title": ["Product does not exist "]
                })

            if str(product.pk) not in basket.basket:
                return Response({
                    "product_title": ["This product is not in the basket"]
                })

            basket.update(product=product, product_qty=qty)

            response = {
                'status': 'Product updated',
                'total_qty': basket.get_basket_qty,
                'total_price': basket.get_basket_price,
            }

            return Response(response)


@api_view(['GET'])
def api_basket_view(request):
    basket = Basket(request)

    response = {}
    for pk, item_detail in basket.basket.items():
        title = item_detail['title']
        response[title] = item_detail

    return Response(response)

