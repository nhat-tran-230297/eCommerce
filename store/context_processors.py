from django.conf import settings

from .models import Category, Product


def categories(request) -> dict:
    return { 
        'categories_context_processor': Category.objects.all() 
    }

def products(request) -> dict:
    return { 
        'products_context_processor': Product.active_products.all() 
    }


def currency(request) -> dict:
    return {
        'currency_context_processor' : settings.CURRENCY
    }

