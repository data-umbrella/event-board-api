import json

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token

from drfpasswordless.utils import CallbackToken

User = get_user_model()

class RegistrationAPITest(TestCase):
    """ Test module for passwordless authentication"""

    def setUp(self):
        self.email = 'janesmith@example.com'
        self.url = '/auth/email/'

    # curl -X POST -d "email=example@example.com" localhost:8000/auth/email/
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

    # curl -X POST -d "email=example@example.com&token=815381" localhost:8000/auth/token/
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

    def tearDown(self):
        self.user.delete()
