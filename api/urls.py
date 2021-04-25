from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'api'

urlpatterns = [
    # Product
    path('product/', views.APIProductListView.as_view(), name='product_list'),
    path('product/create/', views.APIProductCreateView.as_view(), name='product_create'),
    path('product/<slug:slug>/', views.APIProductDetailView.as_view(), name='product_detail'),
    
    # Category
    path('category/', views.APICategoryListView.as_view(), name='category_product_list'),

    # Basket 
    path('basket/', views.APIBasketView.as_view(), name='basket'),
    path('basket/add/', views.APIBasketAddView.as_view(), name='basket_add'),
    path('basket/remove/', views.APIBasketRemoveView.as_view(), name='basket_remove'),
    path('basket/update/', views.APIBasketUpdateView.as_view(), name='basket_update'),

    # login
    path('login/', obtain_auth_token, name='api_login')

]