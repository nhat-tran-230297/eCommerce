from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from account.models import UserBase
from store.models import Category, Product


# Create your tests here.
class TestAPIProductView(APITestCase):
    def setUp(self):
        self.user1 = UserBase.objects.create_user(
            email='admin@gmail.com', username='admin',  password='admin', 
            is_active=True, is_staff=True)
        self.category1 = Category.objects.create(name='e-courses', slug='e-courses')
        self.product1 = Product.objects.create(
            category_id=1, 
            title='Django beginners',
            product_code='code1',
            product_creator_id=1,
            slug='django-beginners',
            price='20.00',
        )


    def test_api_product_list_view(self):
        self.client.login(email='admin@gmail.com', password='admin')

        response = self.client.get(
            reverse('api:product_list'), 
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # def test_api_product_detail_view(self):
    #     self.client.login(email='admin@gmail.com', password='admin')

    #     response = self.client.get(
    #         reverse('api:product_detail', kwargs={'slug': 'django-beginners'}), 
    #         format='json'
    #     )

    #     print(response)

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    # def test_api_product_create_view(self):
    #     self.client.login(email='admin@gmail.com', password='admin')

    #     data = {
    #         'title': 'django basic', 'product_code': '123', 
    #         'category': 'e-courses', 'product_creator': 'admin', 'price': 0.99
    #     }
    #     response = self.client.post(
    #         reverse('api:product_create'),
            
    #         format='json',

    #     )