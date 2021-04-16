from account.models import UserBase
from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product


# Create your tests here.
class TestCategoryModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name="django", slug="django")

    def test_category_model_entry(self):
        """
        Test Category model data field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), "django")

    # def test_category_url(self):
    #     """
    #     Test category model slug and URL reverse
    #     """
    #     data = self.data1
    #     response = self.client.post(
    #         reverse('store:category_list', args=[data.slug]))
    #     self.assertEqual(response.status_code, 200)


class TestProductModel(TestCase):
    def setUp(self):
        Category.objects.create(name="django", slug="django")
        UserBase.objects.create(username="aimblaster")
        self.data1 = Product.objects.create(
            category_id=1,
            title="django beginners",
            product_creator_id=1,
            slug="django-beginners",
            price="20.00",
            image="django",
        )

        # self.data2 = Product.products.create(
        #         category_id=1,
        #         title='django advanced',
        #         product_creator_id=1,
        #         slug='django-advanced',
        #         price='20.00',
        #         image='django',
        #         is_active=False)

    def test_product_model_entry(self):
        """
        Test product model data field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), "django beginners")
