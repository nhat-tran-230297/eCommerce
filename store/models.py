from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        # as default, on the admin page is 'Categorys' -> overwrite to 'categories'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('store:category_list', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE) 
    product_creator = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    is_instock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    # auto_now_add: trigger only once
    # auto_now  : trigger everytime there is an update
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        # order of products: latest -> oldest
        ordering = ('-created_time',)

    def get_absolute_url(self):
        return reverse('store:product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title