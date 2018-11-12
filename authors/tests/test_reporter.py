from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from .base_test import BaseTest

from ..apps.authentication.models import User

class TestReporter(BaseTest):

    def test_if_an_article_can_be_reported(self):
        
        response = self.client.post("/api/articles/{}/report/".format(self.slug), self.report_data, **self.headers)
        self.assertEqual(response.status_code, 201)