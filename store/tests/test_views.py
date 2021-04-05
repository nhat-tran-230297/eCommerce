from importlib import import_module
from unittest import skip

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse

from store import views
from store.models import Category, Product


@skip('demonstrating skipping')
class TestSkip(TestCase):
    def test_skip_example(self):
        pass

class TestViewResponses(TestCase):
    def setUp(self):
        User.objects.create(username='admin')
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
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)


    def test_home_page_url(self):
        url = '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        url = reverse('store:product_detail', kwargs={'slug': 'django-beginners'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_list_url(self):
        url = reverse('store:category_list', kwargs={'category_slug': 'django'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    
    def test_homepage_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()

        response = views.product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>CourseStore</title>', html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    
    # def test_view_function(self):
    #     request = self.factory.get('/django-beginners')
    #     response = views.product_all(request)
        
    #     html = response.content.decode('utf8')
    #     self.assertIn('<title>CourseStore</title>', html)
    #     self.assertTrue(html.startswith('\n\n<!DOCTYPE html>\n'))
    #     self.assertEqual(response.status_code, 200)
