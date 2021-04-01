from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product


class TestBasketView(TestCase):
    def setUp(self):
        User.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(category_id=1, title='django beginners',     product_creator_id=1,
                               slug='django-beginners', price='20.00', image='django')
        
        Product.objects.create(category_id=1, title='django intermediate', product_creator_id=1,
                               slug='django-intermediate', price='20.00', image='django')
        
        Product.objects.create(category_id=1, title='django advanced', product_creator_id=1,
                               slug='django-advanced', price='20.00', image='django')

    
        # add item to the basket
        self.client.post(
            path=reverse('basket:basket_add'), 
            data={"productID": 1, "productQty": 1, "action": "post"}, 
            xhr=True)

        # add item to the basket
        self.client.post(
            path=reverse('basket:basket_add'), 
            data={"productID": 2, "productQty": 2, "action": "post"}, 
            xhr=True)

        # there is a total of 3 products in the basket


    def test_basket_url(self):
        """
        Test basket summary url
        """

        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 200)

    
    def test_basket_add(self):
        """
        Test adding items to the session basket
        """
        
        # add new product to basket
        response = self.client.post(
            path=reverse('basket:basket_add'),
            data={'productID': 3, 'productQty': 1, 'action': 'post'},xhr=True)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['basket_qty'], 4)
        self.assertEqual(data['basket_price'], '80.00')

        # update product already in basket 
        response = self.client.post(
            path=reverse('basket:basket_add'),
            data={'productID': 3, 'productQty': 2, 'action': 'post'},xhr=True)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['basket_qty'], 6)
        self.assertEqual(data['basket_price'], '120.00')


    def test_basket_delete(self):
        """
        Test deleting items from the session basket
        """
        response = self.client.post(
            path=reverse('basket:basket_delete'),
            data={'productID': 2, 'action': 'delete'},
            xhr=True
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['basket_qty'], 1)
        self.assertEqual(data['basket_price'], '20.00')