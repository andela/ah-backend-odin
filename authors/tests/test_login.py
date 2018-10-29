from django.test import TestCase, Client

class TestLogin(TestCase):
    def setUp(self):
        self.client = Client(content_type="application/json")
        self.user = {
            "email": "jake@jake.jake",
            "password": "jakejake"
        }
    
    def test_login_user_returns_201_status_code(self):
        response = self.client.post("/api/users/login/", self.user)
        self.assertEqual(response.status_code, 200)