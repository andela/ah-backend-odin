from django.test import TestCase
from rest_framework.test import APIClient


class TestAuthentication(TestCase):
    def setUp(self):
        self.client = APIClient(content_type="application/json")
        self.user_data = {
            "user": {
                "email": "johndoe@example.com",
                "username": "johndoe",
                "password": "password"
            }
        }

    def create_user(self):
        return self.client.post("/api/users/", self.user_data)

      
    def login_user(self):
        self.create_user()
        return self.client.post("/api/users/login/", self.user_data)

    def test_create_users_returns_201_status_code(self):
        response = self.create_user()
        self.assertEqual(response.status_code, 201)

    def test_create_user_response_has_username(self):
        response = self.create_user()
        self.assertEqual(
            response.data['username'],
            self.user_data["user"]["username"]
        )
    def test_successfull_user_registeration_response_has_token(self):
        response = self.create_user()
        self.assertIn('token', response.data)

    def test_login_user_returns_200_status_code(self):
        response = self.login_user()
        self.assertEqual(response.status_code, 200)

    def test_successfull_login_response_has_token(self):
        response = self.login_user()
        self.assertIn('token', response.data)

