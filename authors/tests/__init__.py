from django.test import TestCase
from rest_framework.test import APIClient
from authors.apps.authentication.models import User


class BaseAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient(content_type="application/json")
        self.default_user = {
            "email": "johndoe@example.com",
            "username": "johndoe",
            "password": "Password123"
        }

    def login_user_endpoint(self):
        self.create_user()
        return self.client.post(
            "/api/users/login/",
            dict(user=self.default_user)
        )

    def create_user(self, data=None):
        user = {"user": data or self.default_user}
        return self.client.post("/api/users/", user)

    def authenticate(self, user=None):
        user = user or dict(
            username="authuser",
            password="password",
            email="roland@example.com",

        )
        user['is_active'] = True
        user_model = User.objects.create(**user)
        self.client.force_authenticate(user=user_model)
        return user_model

    def tearDown(self):
        super().tearDown()
        # remove the token so that it doesn't affect the tests
        # that don't require it
        self.client.logout()
