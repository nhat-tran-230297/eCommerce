from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_view'),
    path('product/<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:category_slug>', views.CategoryProductListView.as_view(), name='category_product_list'),
    path('search/', views.ProductSearchResultsView.as_view(), name='product_search_results'),
]
