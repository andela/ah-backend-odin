from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnList
from .base_test import BaseTest


class ArticlesTest(BaseTest):

    def test_create_article(self):
        response = self.create_article()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('title', response.data)

    def test_get_articles(self):
        response = self.get_article()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.data, ReturnList))

    def test_get_one_article(self):
        response = self.get_one_article()
        self.assertEqual(response.status_code, 200)

    def test_delete_article(self):
        self.create_article()
        response = self.delete_article()
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.data)
        self.assertEqual(response.json()['message'],
                         'Article is deleted')

    def test_update_article(self):
        self.create_article()
        response = self.update_article()
        self.assertEqual(response.status_code, 201)
