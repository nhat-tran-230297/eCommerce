# from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from account.models import UserBase


class ProductActiveManager(models.Manager):
    """
    Custom Manager for products, where is_active=True
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class ProductInstockManager(models.Manager):
    """
    Custom Manager for products, where is_instock=True
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_instock=True)


# Create your models here.
class Category(models.Model):
    """
    Category Model
    """

    name = models.CharField(max_length=255, db_index=True, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        # as default, on the admin page is 'Categorys' -> overwrite to 'Categories'
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse("store:category_product_list", kwargs={"category_slug": self.slug})

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product Model
    """

    category = models.ForeignKey(Category, related_name="product", on_delete=models.PROTECT)
    product_creator = models.ForeignKey(UserBase, related_name="products", on_delete=models.CASCADE)
    
    title = models.CharField(max_length=255, unique=True)
    product_code = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=255, default="admin")
    
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/", default="images/default.png")
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_instock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    # auto_now_add: trigger only once
    # auto_now  : trigger everytime there is an update
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    # custom Manager #
    objects = models.Manager()  # The default manager.
    active_products = ProductActiveManager()  # active_products specific manager
    instock_products = ProductInstockManager()  # instock_products specific manager

    # detect whenever title changes
    __original_title = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_title = self.title

    
    class Meta:
        # order of products: latest -> oldest
        ordering = ("-created_time",)


    def get_absolute_url(self):
        """
        url of detail-view of each product
        """
        return reverse("store:product_detail", kwargs={"slug": self.slug})

    @property
    def get_api_url(self):
        relative_url = reverse("api:product_detail", kwargs={"slug": self.slug})

        return f'{settings.DOMAIN}{relative_url}'

       

    @staticmethod
    def _check_unique_slug(slug):
        """
        Generate a new slug when the current slug exists in the database.
        If not exists, the current slug remains unchanged
        """

        new_slug = slug
        while Product.objects.filter(slug=new_slug).exists():
            new_slug = slug + '-' + get_random_string(length=5)

        return new_slug
    

    def save(self, *args, **kwargs):    
        """
        Override save() method
        Check whether slug is unique when create or updating product
        """

        slug_title = slugify(self.title)
        if not self.slug:
            # when creating new product
            self.slug = self._check_unique_slug(slug_title)

        else:
            # when updating product
            if self.title != self.__original_title:
                # when title is updated, check the slug 
                self.slug = self._check_unique_slug(slug_title)
        

        super().save(*args, **kwargs)
        self.__original_title = self.title


    

    def __str__(self):
        return self.title
