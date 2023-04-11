import json
from http.cookies import SimpleCookie
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from drfpasswordless.utils import CallbackToken
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegistrationAPITest(TestCase):
    """ Test module for passwordless authentication"""

    def setUp(self):
        self.email = 'janesmith@example.com'
        self.url = '/auth/email/'

    def test_auth_registration_request(self):
        data = {'email': self.email}

        # Verify user doesn't exist yet
        user = User.objects.filter(**{'email': 'janesmith@example.com'}).first()
        # Make sure our user isn't None, meaning the user was created.
        self.assertEqual(user, None)

        # verify a new user was created with serializer
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(**{'email': self.email})
        self.assertNotEqual(user, None)

        # Verify a token exists for the user
        self.assertEqual(CallbackToken.objects.filter(user=user, is_active=True).exists(), 1)

class ConfirmationAPITest(TestCase):

    def setUp(self):
        self.email = 'janesmith@example.com'
        self.url = '/auth/email/'
        self.challenge_url = '/auth/token/'
        self.user = User.objects.create(**{'email': self.email})
    
    def tearDown(self):
        self.user.delete()

    def test_email_auth_success(self):
        data = {'email': self.email}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Token sent to alias
        callback_token = CallbackToken.objects.filter(user=self.user, is_active=True).first()
        challenge_data = {'email': self.email, 'token': callback_token}

        # Try to auth with the callback token
        challenge_response = self.client.post(self.challenge_url, challenge_data)
        self.assertEqual(challenge_response.status_code, status.HTTP_200_OK)

        # Verify Auth Token
        auth_token = challenge_response.data['token']
        self.assertEqual(auth_token, Token.objects.filter(key=auth_token).first().key)


class CurrentUserAPITest(TestCase):

    def setUp(self):
        self.email = 'janesmith@example.com'
        self.registration_url = '/auth/email/'
        self.challenge_url = '/auth/token/'
        self.current_user_url = '/api/v1/current_user/'
        self.user = User.objects.create(**{'email': self.email})
    
    def tearDown(self):
        self.user.delete()

    def generate_auth_token(self):
        self.client.post(self.registration_url, {'email': self.email})
        callback_token = CallbackToken.objects.filter(user=self.user, is_active=True).first()
        challenge_response = self.client.post(self.challenge_url, {
            'email': self.email,
            'token': callback_token,
        })
        return challenge_response.data['token']

    def test_current_user_with_http_cookies_success(self):
        current_user_response = self.client.post(
            self.current_user_url,
            content_type='application/json',
            HTTP_COOKIE=f"access_token={self.generate_auth_token()}",
        )

        self.assertEqual(current_user_response.status_code, status.HTTP_200_OK)
        self.assertEqual(current_user_response.data['email'], self.email)
        self.assertEqual(current_user_response.data['email_verified'], True)

    def test_current_user_with_http_auth_header_success(self):
        current_user_response = self.client.post(
            self.current_user_url,
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Token {self.generate_auth_token()}",
        )

        self.assertEqual(current_user_response.status_code, status.HTTP_200_OK)


class DeleteUserAPITest(TestCase):

    def setUp(self):
        self.email = 'janesmith@example.com'
        self.registration_url = '/auth/email/'
        self.challenge_url = '/auth/token/'
        self.delete_account_url = '/api/v1/delete_account/'
        self.user = User.objects.create(**{'email': self.email})

    def tearDown(self):
        self.user.delete()

    def generate_auth_token(self):
        self.client.post(self.registration_url, {'email': self.email})
        callback_token = CallbackToken.objects.filter(user=self.user, is_active=True).first()
        challenge_response = self.client.post(self.challenge_url, {
            'email': self.email,
            'token': callback_token,
        })
        return challenge_response.data['token']

    def test_delete_user_with_http_cookies_success(self):
        delete_account_response = self.client.delete(
            self.delete_account_url,
            content_type='application/json',
            HTTP_COOKIE=f"access_token={self.generate_auth_token()}",
        )

        self.assertEqual(delete_account_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_with_http_auth_header_success(self):
        delete_account_response = self.client.delete(
            self.delete_account_url,
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Token {self.generate_auth_token()}",
        )
        self.assertEqual(delete_account_response.status_code, status.HTTP_204_NO_CONTENT)
