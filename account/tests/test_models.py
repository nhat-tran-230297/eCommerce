from django.test import TestCase

from account.models import UserBase


# Create your tests here.
class TestUserBaseModel(TestCase):
    def setUp(self):
        self.user1 = UserBase.objects.create(username='admin', email='admin@gmail.com', password='admin')


    def test_unactivated_user(self):
        self.assertEqual(self.user1.is_active, False)


        
