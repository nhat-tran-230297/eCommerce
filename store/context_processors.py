from django.conf import settings

from .models import Category


def categories(request) -> dict:
    return { 
        'categories_context_processor': Category.objects.all() 
    }


def currency(request) -> dict:
    return {
        'currency_context_processor' : settings.CURRENCY
    }

