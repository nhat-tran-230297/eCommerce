from django.shortcuts import get_object_or_404, render

from .models import Category, Product

# Create your views here.


def product_all(request):
    """
    Home page - display all active products
    """

    products = Product.active_products.all()

    context = {"products": products}
    return render(request, "store/home.html", context)


def product_detail(request, slug:str):
    """
    Product detail view
    """

    product = get_object_or_404(Product, slug=slug, is_instock=True)

    context = {"product": product}
    return render(request, "store/product/detail.html", context)


def category_list(request, category_slug:str):
    """
    Category list view (lists of products regarding the category)
    """

    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)

    context = {
        "category": category,
        "products": products,
    }
    return render(request, "store/product/category.html", context)
