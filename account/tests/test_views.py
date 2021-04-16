from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from account.models import UserBase


# Create your tests here.
class TestAccountView(TestCase):
    def setUp(self):
        self.user1 = UserBase.objects.create_user(email='admin@gmail.com', username='admin',  password='admin')


    def test_unactivated_user_view(self):
        is_logged_in = self.client.login(email='admin@gmail.com', password='asadmin')

        self.assertEqual(self.user1.is_active, False)
        self.assertEqual(is_logged_in, False)


    def test_dashboard_view(self):
        self.user1.is_active = True
        self.user1.save()

        is_logged_in = self.client.login(email='admin@gmail.com', password='admin')

        response = self.client.get(reverse('account:dashboard'))

        self.assertEqual(self.user1.is_active, True)
        self.assertEqual(is_logged_in, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
