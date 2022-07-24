import json
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from drfpasswordless.utils import CallbackToken
from rest_framework import status
from rest_framework.authtoken.models import Token
from events.models import Event


User = get_user_model()

class ListEventsAPITest(TestCase):
    """ Test module for event list """

    def event_title(self):
        return 'Example Title'

    def setUp(self):
        Event.objects.create(
            title=self.event_title(),
            description='Example Description #1',
            featured=False,
        )
        Event.objects.create(
            title='Big Event Title',
            description='Big Event Description',
            featured=True,
        )

    def test_event_get_request(self):
        client = Client()
        response = client.get('/api/v1/events')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data[0]['title'], self.event_title())

    def test_event_filter_description_request(self):
        client = Client()
        response = client.get('/api/v1/events?search=Big%20Event%20Description')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['title'], 'Big Event Title')

    def test_event_filter_title_request(self):
        client = Client()
        response = client.get('/api/v1/events?search=Big%20Event%20Title')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['title'], 'Big Event Title')

    def test_event_filter_featured_request(self):
        client = Client()
        response = client.get('/api/v1/events?featured=True')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['title'], 'Big Event Title')


class CreateEventAPITest(TestCase):

    def setUp(self):
        self.email = 'janesmith@example.com'
        self.url = '/auth/email/'
        self.challenge_url = '/auth/token/'
        self.user = User.objects.create(**{'email': self.email})
        data = {'email': self.email}
        self.client.post(self.url, data)

        callback_token = CallbackToken.objects.filter(user=self.user, is_active=True).first()
        challenge_data = {'email': self.email, 'token': callback_token}
        challenge_response = self.client.post(self.challenge_url, challenge_data)
        self.auth_token = challenge_response.data['token']

    def test_authenticated_event_post_request(self):
        request_data = {
            'title': 'Post Event Title',
            'description': 'Post Event Description',
            'featured': 'False',
        }
        response = self.client.post(
            '/api/v1/events',
            json.dumps(request_data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.auth_token}",
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['title'], request_data['title'])

    def test_unauthenticated_event_post_request(self):
        request_data = {
            'title': 'Post Event Title',
            'description': 'Post Event Description',
            'featured': 'False',
        }
        response = self.client.post(
            '/api/v1/events',
            json.dumps(request_data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token BAD_TOKEN",
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        self.user.delete()
