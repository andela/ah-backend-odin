from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
from .base_test import BaseTest


class CommentTest(BaseTest):

    def test_create_comment(self):
        """Test user can create a comment"""
        self.create_article()
        response = self.create_comment()
        self.assertEqual(response.status_code, 201)

    def test_delete_comment(self):
        """Test user can delete a comment"""
        self.create_article()
        response = self.delete_comment()
        self.assertEqual(response.status_code, 200)   

    def test_comment_on_non_existing_article(self):
        """Test system returns 400 error code when article doesnt exist"""
        self.create_article()
        response = self.comment_on_non_existing_article()
        self.assertEqual(response.status_code, 400)          


    def test_create_thread(self):
        """Test system can thread comments"""
        self.create_article()
        self.create_comment()
        response = self.create_thread()
        self.assertEqual(response.status_code, 201)

class CommentLikeTests(BaseTest):

    def test_like_comment(self):
        response = self.like_comment()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_dislike_comment(self):
        response = self.dislike_comment()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_double_like_comment(self):
        response = self.double_like_comment()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
