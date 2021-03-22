from unittest import skip

from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from store.models import Category, Product



@skip('demonstrating skipping')
class TestSkip(TestCase):
    def test_skip_example(self):
        pass

class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        User.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(
            category_id=1, 
            title='django beginners',
            product_creator_id=1,
            slug='django-beginners',
            price='20.00',
            image='django'
        )

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    
    def test_product_detail_url(self):
        response = self.c.get(reverse('store:product_detail', kwargs={'slug': 'django-beginners'}),)
        self.assertEqual(response.status_code, 200)