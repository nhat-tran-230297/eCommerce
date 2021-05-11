from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from account.models import UserBase


class TestAPIUserAuthentication(APITestCase):
    def setUp(self):
        self.user1 = UserBase.objects.create_user(
            email='admin@gmail.com', username='admin',  password='admin', 
            is_active=True
        )

    
    def test_login_success(self):
        is_logged_in = self.client.login(email='admin@gmail.com', password='admin')

        response = self.client.get(
            reverse('api:product_list'), 
            format='json'
        )

        self.assertEqual(is_logged_in, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)