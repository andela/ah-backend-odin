import os
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnList
from .base_test import BaseTest

class ArticlesTest(BaseTest):
    
    # def test_valid_google_login(self):
    #     response = self.client.post('/api/google_login/', self.google_social_login)
    #     self.assertEqual(response.status_code, 200)

    def test_valid_facebook_login(self):
        response = self.client.post('/api/facebook_login/', self.facebook_social_login)
        self.assertEqual(response.status_code, 200) 

    def test_invalid_facebook_login(self):
        response = self.client.post('/api/facebook_login/', {"user":{"access_token": os.environ.get("FACEBOOK_INVALID_TOKEN", None)}})
        self.assertEqual(response.status_code, 400)  

    def test_invalid_gooogle_login(self):
        response = self.client.post('/api/google_login/', {"user":{"access_token": os.environ.get("GOOGLE_INVALID_TOKEN", None)}})
        self.assertEqual(response.status_code, 400)                 


    

    


