from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        TestCase.assertEqual(self, path, '/')
        TestCase.assertTemplateUsed(self, response, 'products/index.html')


class ProductsListTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def _common_test(self, arg):
        self.assertEqual(arg.status_code, 200)
        self.assertTemplateUsed(arg, 'products/products.html')
        self.assertEqual(arg.context_data['title'], 'Store-Catalog')

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)
        self._common_test(response)


