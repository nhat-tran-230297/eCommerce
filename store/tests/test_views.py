from importlib import import_module

from account.models import UserBase
from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from store import views
from store.models import Category, Product


class TestViewResponses(TestCase):
    def setUp(self):
        UserBase.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(
            category_id=1, 
            title='Django beginners',
            product_creator_id=1,
            slug='django-beginners',
            price='20.00',
            image='django'
        )

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.client.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get('/', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_home_page_url(self):
        url = '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_url(self):
        url = reverse('store:product_detail', kwargs={'slug': 'django-beginners'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_list_url(self):
        url = reverse('store:category_list', kwargs={'category_slug': 'django'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_homepage_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()

        response = views.product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>CourseStore</title>', html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


