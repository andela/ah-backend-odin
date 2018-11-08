from django.test import TestCase
from rest_framework.test import APIClient


class BaseAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient(content_type="application/json")
        self.default_user = {
            "email": "johndoe@example.com",
            "username": "johndoe",
            "password": "Password123"

        }

    def login_user(self):
        self.create_user()
        return self.client.post(
            "/api/users/login/",
            dict(user=self.default_user)
        )

    def create_user(self, data=None):
        user = {"user": data or self.default_user}
        return self.client.post("/api/users/", user)
