from django.test import TestCase
from rest_framework.test import APIClient
import json


class BaseTest(TestCase):
    def setUp(self):
        self.client = APIClient(content_type="application/json")
        self.user_data = {
            "user": {
                "email": "johndoe@example.com",
                "username": "johndoe",
                "password": "Password123"
            }
        }

        self.user_data2 = {
            "user": {
                "email": "odin@example.com",
                "username": "odin",
                "password": "Password123"
            }
        }

        self.article_data = {
            "article": {
                "title": "some title",
                "description": "Some description",
                "body": "some story here",
                "tagList": ["mother", "love"],
                "published":"True"
            }
        }

        self.article_data2 = {
            "article": {
                "title": "some title",
                "description": "Some description needed here",
                "body": "some story here",
                "tagList": ["mother", "love"],
                "published":"True"
            }
        }

        self.report_data = {"report" : 
                                {
                                    "reason" : "this is a plagiarized article"
                                }
                            }
        self.article_like_data = {
                "article": {
		            "article_like":"True"
	            }
        }


        self.article_dislike_data = {
                "article": {
		            "article_like":"True" 
	            }
        }
        
        self.report_data2 = {"report" : 
                                {
                                    "reason" : ""
                                }
                            }

        self.report_data3 = {"object" : 
                                {
                                    "reason" : "this is a plagized article"
                                }
                            }
        
        self.token = dict(self.login_user().data)['token']
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        self.slug = dict(self.create_article().data)['slug']
        


    def create_user(self):
        return self.client.post("/api/users/", self.user_data)

      
    def login_user(self):
        self.create_user()
        return self.client.post("/api/users/login/", self.user_data)
    
    def login_user2(self):
        self.create_user()
        return self.client.post("/api/users/login/", self.user_data2)

    def create_article(self):
        return self.client.post("/api/articles/", self.article_data, **self.headers)
    
    def get_article(self):
        return self.client.get("/api/articles/", self.article_data, **self.headers)
    
    def get_one_article(self):
        return self.client.get(f"/api/articles/{self.slug}", self.article_data, **self.headers)

    def delete_article(self):
        return self.client.delete(f"/api/articles/{self.slug}", self.article_data, **self.headers)
    
    def update_article(self):
        return self.client.put(f"/api/articles/{self.slug}", self.article_data, **self.headers)
    
    def bookmark_article(self):
        return self.client.post(f"/api/articles/{self.slug}/bookmark", **self.headers)
    def like_article(self):
        return self.client.post(f"/api/articles/{self.slug}/likes", self.article_like_data, **self.headers)
    
    def dislike_article(self):
        return self.client.post(f"/api/articles/{self.slug}/likes", self.article_dislike_data, **self.headers)
    
    def double_like_article(self):
        return self.client.post(f"/api/articles/{self.slug}/likes", self.article_dislike_data, **self.headers)
  
    def get_articles_with_reading_time(self):
        return self.client.get("/api/articles/readings/", self.article_data, **self.headers)
  
    def get_article_with_reading_time(self):
        return self.client.get(f"/api/articles/{self.slug}/readings/", self.article_data, **self.headers)
    