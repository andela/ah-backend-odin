from django.test import TestCase
from rest_framework.test import APIClient
import json


class TestAuthentication(TestCase):
    def setUp(self):
        self.client = APIClient(content_type="application/json")
        self.user_data = {
            "user": {
                "email": "johndoe@example.com",
                "username": "johndoe",
                "password": "Password123"
            }
        }

    def create_user(self):
        return self.client.post("/api/users/", self.user_data)

    def test_create_users_returns_201_status_code(self):
        response = self.client.post("/api/users/", self.user_data)
        self.assertEqual(response.status_code, 201)
    
    def test_login_user_returns_200_status_code(self):
        self.create_user()
        response = self.client.post("/api/users/login/", self.user_data)
        self.assertEqual(response.status_code, 200)
     
    def test_existing_user_email_validation_error_message(self):
        self.create_user()
        response=self.client.post("/api/users/",{"user":{"email":"johndoe@example.com"}} )
        self.assertEqual(response.json()['errors']['email'], [
                         u'Email already in use'])
    
    def test_existing_user_name_validation_error_message(self):
        self.create_user()
        response=self.client.post("/api/users/",{"user":{"username":"johndoe"}} )
        self.assertEqual(response.json()['errors']['username'], [
                         u'Username already in use'])
    
    def test_password_without_an_integer_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"password":"password"}} )
        self.assertEqual(response.json()['errors']['password'], [
                         u'Weak password. Include atleast one integer'])
    
    def test_invalid_email_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"email":"johndoeexamplecom"}} )
        self.assertEqual(response.json()['errors']['email'], [
                         u'Enter a valid email address.'])
    
    def test_all_lower_cased_password_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"password":"password123"}} )
        self.assertEqual(response.json()['errors']['password'], [
                         u'Password should contain both upper and lower cases'])
    
    def test_all_integer_password_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"password":"12345678"}} )
        self.assertEqual(response.json()['errors']['password'], [
                         u'Password can not contain only integers'])

    def test_short_password_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"password":"pass12"}} )
        self.assertEqual(response.json()['errors']['password'], [
                         u'Weak password. Password should be atleast 8 characters long'])

    def test_password_more_than_25_characters_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"password":"PasswordOdin12345567890qtvscvgsffsgfsf"}} )
        self.assertEqual(response.json()['errors']['password'], [
                         u'Password can not be more than 25 caharacters'])
    
    def test_invalid_username_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"username":"@!#$%&"}} )
        self.assertEqual(response.json()['errors']['username'], [
                         u'Invalid characters not allowed'])

    def test_too_short_username_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"username":"su"}} )
        self.assertEqual(response.json()['errors']['username'], [
                         u'Username should be between 3 to 25 characters long'])
