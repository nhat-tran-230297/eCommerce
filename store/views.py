from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .models import Category, Product

# Create your views here.


class HomeView(generic.ListView):
    """
    Home page - display all active products
    """

    model = Product
    queryset = Product.active_products.all()
    template_name = 'store/home.html'
    context_object_name = 'products'

    # pagination
    paginate_by = 15


class ProductDetailView(generic.DetailView):
    """
    Product detail view
    """

    model = Product
    template_name = 'store/product/product_detail.html'
    context_object_name = 'product'


class CategoryProductListView(generic.ListView):
    """
    Category list view (lists of products regarding the category)
    """

    template_name = 'store/category/category_product_list.html'
    context_object_name = 'products'
    paginate_by = 15


    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])

        return Product.objects.filter(category=self.category)


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add 'category' to context data
        context['category'] = self.category

        return context


class ProductSearchResultsView(generic.ListView):
    """
    Search Results
    """

    template_name = 'store/product/product_search_results.html'
    context_object_name = 'search_results'
    paginate_by = 15


    def get_queryset(self):
        self.search_input = self.request.GET['search_input']
        search_results = Product.active_products.filter(title__icontains=self.search_input)
        self.count = search_results.count()

        return search_results


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        context['search_input'] = self.search_input
        context['count'] = self.count

        return context


