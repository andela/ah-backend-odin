from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from .base_test import BaseTest

from authors.apps.profiles.models import Profile
from authors.apps.follower.models import Follow
from authors.apps.authentication.models import User

class TestFollower(TestCase):

    def setUp(self):

        

        self.client = APIClient(content_type="application/json")

        self.user_data2 = {
                "user": {
                    "email": "odin@example.com",
                    "username": "odin",
                    "password": "Password123"
                }
            }

        self.user_data3 = {
            "user": {
                "email": "odon@example.com",
                "username": "odon",
                "password": "Password123"
                    }
                        }

        def create_user():
            return self.client.post("/api/users/", self.user_data2)

        def create_user2():
            return self.client.post("/api/users/", self.user_data3)

        def login_user():
            create_user()
            create_user2()
            return self.client.post("/api/users/login/", self.user_data2)

        
        self.token = dict(login_user().data)['token']
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

    

    def test_if_a_user_can_be_followed(self):
        response = self.client.post("/api/profiles/odon/follow/", **self.headers)
        self.assertEqual(response.status_code, 201)

    def test_if_a_user_can_unfollow(self):
        response = self.client.delete("/api/profiles/odon/unfollow/", **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_if_a_user_can_view_followers(self):
        response = self.client.get("/api/profiles/followers/", **self.headers)
        self.assertEqual(response.status_code, 200)