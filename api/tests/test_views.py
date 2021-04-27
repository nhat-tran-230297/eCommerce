from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase


# Create your tests here.
class TestAPIProductView(APITestCase):
    def setUp(self):
        self.user1 = UserBase.objects.create_user(email='admin@gmail.com', username='admin',  password='admin', is_active=True)

    def test_api_product_list_view(self):
        self.client.login(email='admin@gmail.com', password='admin')

        response = self.client.get(
            reverse('api:product_list'), 
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_api_product_detail_view(self):
        self.client.login(email='admin@gmail.com', password='admin')

        response = self.client.get(
            reverse('api:product_detail'), 
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)