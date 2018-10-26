from django.test import TestCase, Client


class TestAuthentication(TestCase):
    def setUp(self):
        self.client = Client(content_type="application/json")
        self.user = {
            "username": "johndoe",
            "password": "password",
            "email": "johndoe@example.com"
        }

    def test_create_users_returns_201_status_code(self):
        response = self.client.post("/api/users/", self.user)
        self.assertEqual(response.status_code, 200)
