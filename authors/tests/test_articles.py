from rest_framework import status
from rest_framework.utils.serializer_helpers import OrderedDict
from .base_test import BaseTest


class ArticlesTest(BaseTest):

    def test_create_article(self):
        response = self.create_article()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('title', response.data)

    def test_get_articles(self):
        response = self.get_article()
        self.assertEqual(response.status_code, 200)

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

class BookMarkTest(BaseTest):


    def test_bookmark_article(self):
        response = self.bookmark_article()
        self.assertEqual(response.status_code, 200)


class ArticleLikeTests(BaseTest):

    def test_like_article(self):
        response = self.like_article()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_dislike_article(self):
        response = self.dislike_article()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_double_like_article(self):
        response = self.double_like_article()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class TestReadingTime(BaseTest):

    def test_articles_return_reading_time(self):

        self.create_article()

        self.create_article()

        self.create_article()

        response = self.get_articles_with_reading_time()

        self.assertEqual(response.status_code, 200)

    def test_article_return_reading_time(self):

        self.create_article()

        response = self.get_article_with_reading_time()

        self.assertEqual(response.status_code, 404)

    def test_articles_return_reading_time(self):

        self.create_article()

        self.create_article()

        response = self.get_articles_with_their_reading_time()

        self.assertEqual(response.status_code, 200)