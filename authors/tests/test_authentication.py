from django.test import TestCase
from rest_framework.test import APIClient
<<<<<<< HEAD
import json
=======
>>>>>>> parent of aaa0d6f... #161340174 Fix failing models again


class TestAuthentication(TestCase):
    def setUp(self):
        self.client = APIClient(content_type="application/json")
        self.user_data = {
            "user": {
                "email": "johndoe@example.com",
                "username": "johndoe",
<<<<<<< HEAD
                "password": "Password123"
=======
                "password": "password"
>>>>>>> parent of aaa0d6f... #161340174 Fix failing models again
            }
        }

    def create_user(self):
        return self.client.post("/api/users/", self.user_data)

<<<<<<< HEAD
      
    def login_user(self):
        self.create_user()
        return self.client.post("/api/users/login/", self.user_data)

=======
>>>>>>> parent of aaa0d6f... #161340174 Fix failing models again
    def test_create_users_returns_201_status_code(self):
        response = self.create_user()
        self.assertEqual(response.status_code, 201)

    def test_create_user_response_has_username(self):
        response = self.create_user()
        self.assertEqual(
            response.data['username'],
            self.user_data["user"]["username"]
        )
<<<<<<< HEAD
    def test_successfull_user_registeration_response_has_token(self):
        response = self.create_user()
        self.assertIn('token', response.data)

    def test_login_user_returns_200_status_code(self):
        response = self.login_user()
        self.assertEqual(response.status_code, 200)
     
    def test_existing_user_email_validation_error_message(self):
        self.create_user()
        response=self.client.post("/api/users/",{"user":{"email":"johndoe@example.com"}} )
        self.assertEqual(response.json()['errors']['email'], [
                        'Email already in use'])
    
    def test_existing_user_name_validation_error_message(self):
        self.create_user()
        response=self.client.post("/api/users/",{"user":{"username":"johndoe"}} )
        self.assertEqual(response.json()['errors']['username'], [
                        'Username already in use'])
    
    def test_password_without_an_integer_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"password":"password"}} )
        self.assertEqual(response.json()['errors']['password'], [
                        'Weak password. Include atleast one integer'])
    
    def test_invalid_email_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"email":"johndoeexamplecom"}} )
        self.assertEqual(response.json()['errors']['email'], [
                        'Enter a valid email address.'])
    
    def test_all_lower_cased_password_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"password":"password123"}} )
        self.assertEqual(response.json()['errors']['password'], [
                        'Password should contain both upper and lower cases'])
    
    def test_all_integer_password_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"password":"12345678"}} )
        self.assertEqual(response.json()['errors']['password'], [
                        'Password can not contain only integers'])

    def test_short_password_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"password":"pass12"}} )
        self.assertEqual(response.json()['errors']['password'], [
                        'Weak password. Password should be atleast 8 characters long'])

    def test_password_more_than_25_characters_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"password":"PasswordOdin12345567890qtvscvgsffsgfsf"}} )
        self.assertEqual(response.json()['errors']['password'], [
                        'Password can not be more than 25 caharacters'])
    
    def test_invalid_username_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"username":"@!#$%&"}} )
        self.assertEqual(response.json()['errors']['username'], [
                        'Invalid characters not allowed'])

    def test_too_short_username_validation_error_message(self):
        response=self.client.post("/api/users/",{"user":{"username":"su"}} )
        self.assertEqual(response.json()['errors']['username'], [
                        'Username should be between 3 to 25 characters long'])

    def test_successfull_login_response_has_token(self):
        response = self.login_user()
        self.assertIn('token', response.data)

=======
>>>>>>> parent of aaa0d6f... #161340174 Fix failing models again
