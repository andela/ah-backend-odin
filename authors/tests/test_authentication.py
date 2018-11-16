from . import BaseAPITestCase
from rest_framework import status
from .base_test import BaseTest


class TestAuthentication(BaseAPITestCase):

    def test_create_users_returns_201_status_code(self):
        response = self.create_user()
        self.assertEqual(response.status_code, 201)

    def test_create_user_response_has_username(self):
        response = self.create_user()
        self.assertEqual(
            response.data['username'],
            self.default_user["username"]
        )

    def test_successfull_user_registeration_response_has_token(self):
        response = self.create_user()
        self.assertIn('token', response.data)

    def test_login_user_returns_200_status_code(self):
        response = self.login_user_endpoint()
        self.assertEqual(response.status_code, 200)

    def test_existing_user_email_validation_error_message(self):
        self.create_user()
        response = self.create_user({"email": "johndoe@example.com"})
        self.assertEqual(
            response.json()['errors']['email'],
            ['Email already in use']
        )

    def test_existing_user_name_validation_error_message(self):
        self.create_user()
        response = self.create_user({"username": "johndoe"})

        self.assertEqual(
            response.json()['errors']['username'],
            ['Username already in use']
        )

    def test_password_without_an_integer_validation_error_message(self):
        response = self.create_user({"password": "password"})
        self.assertEqual(
            response.json()['errors']['password'],
            ['Weak password. Include atleast one integer']
        )

    def test_invalid_email_validation_error_message(self):
        response = self.create_user({"email": "johndoeexamplecom"})
        self.assertEqual(
            response.json()['errors']['email'],
            ['Enter a valid email address.']
        )

    def test_all_lower_cased_password_validation_error_message(self):
        response = self.create_user({"password": "password123"})
        self.assertEqual(
            response.json()['errors']['password'],
            ['Password should contain both upper and lower cases']
        )

    def test_all_integer_password_validation_error_message(self):
        response = self.create_user({"password": "12345678"})
        self.assertEqual(
            response.json()['errors']['password'],
            ['Password can not contain only integers']
        )

    def test_short_password_validation_error_message(self):
        response = self.create_user({"password": "pass12"})
        self.assertEqual(
            response.json()['errors']['password'],
            ['Weak password. Password should be atleast 8 characters long']
        )

    def test_password_more_than_25_characters_validation_error_message(self):
        response = self.create_user(
            {"password": "PasswordOdin12345567890qtvscvgsffsgfsf"}
        )
        self.assertEqual(
            response.json()['errors']['password'],
            ['Password can not be more than 25 caharacters']
        )

    def test_invalid_username_validation_error_message(self):
        response = self.create_user({"username": "@!#$%&"})
        self.assertEqual(
            response.json()['errors']['username'],
            ['Invalid characters not allowed']
        )

    def test_too_short_username_validation_error_message(self):
        response = self.create_user({"username": "su"})
        self.assertEqual(
            response.json()['errors']['username'],
            ['Username should be between 3 to 25 characters long']
        )

    def test_successfull_login_response_has_token(self):
        response = self.login_user_endpoint()
        self.assertIn('token', response.data)


class TestResetPassword(BaseTest):

    def test_get_reset_token(self):

        response = self.get_reset_token()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_send_reset_token_and_link(self):
        self.create_user()
        response = self.create_token_and_send_reset_link()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_implement_password_change(self):
        self.create_user()
        self.create_token_and_send_reset_link()

        response = self.reset_password()

        self.assertEqual(response.status_code, status.HTTP_200_OK)


