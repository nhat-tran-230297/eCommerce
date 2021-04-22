from django.contrib import admin

from .models import Category, Product


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category model admin
    """

    list_display = ['name', 'slug']

    # assign 'slug' field = 'name' field
    prepopulated_fields = {'slug': ('name',)}



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Product model admin
    """

    list_display = ['title', 'product_code', 'author', 'slug', 'price', 'is_instock', 'created_time', 'updated_time']
    list_filter = ['is_instock', 'is_active']
    list_editable = ['price', 'is_instock']

    # assign 'slug' field = 'title' field
    prepopulated_fields = {'slug': ('title',)}
