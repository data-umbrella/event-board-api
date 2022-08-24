import json
import datetime
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

    def event_name(self):
        return 'Example Title'

    def setUp(self):
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.next_week = self.today + datetime.timedelta(days=7)
        self.next_month = self.today + datetime.timedelta(days=40)

        Event.objects.create(
            event_name=self.event_name(),
            description='Example Description #1',
            featured=False,
            start_date=self.today
        )
        Event.objects.create(
            event_name='Big Event Title',
            description='Big Event Description',
            featured=True,
            published=True,
            start_date=self.yesterday,
        )
        Event.objects.create(
            event_name='Future Event Title',
            description='Future Event Description',
            featured=False,
            start_date=self.next_month,
        )

    def test_event_get_request(self):
        client = Client()
        response = client.get('/api/v1/events')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data[0]['event_name'], self.event_name())

    def test_event_filter_description_request(self):
        client = Client()
        response = client.get('/api/v1/events?search=Big%20Event%20Description')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['event_name'], 'Big Event Title')

    def test_event_filter_title_request(self):
        client = Client()
        response = client.get('/api/v1/events?search=Big%20Event%20Title')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['event_name'], 'Big Event Title')

    def test_event_filter_featured_request(self):
        client = Client()
        response = client.get('/api/v1/events?featured=True')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['event_name'], 'Big Event Title')
    
    def test_event_filter_published_request(self):
        client = Client()
        response = client.get('/api/v1/events?published=True')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['event_name'], 'Big Event Title')

    def test_event_filter_by_date_request(self):
        client = Client()
        response = client.get(f"/api/v1/events?start_date={self.today}")
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['event_name'], 'Example Title')

    def test_event_filter_by_date_range_request(self):
        client = Client()
        response = client.get(f"/api/v1/events?start_date__gte={self.yesterday}")
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 3)
        self.assertEqual(response_data[0]['event_name'], 'Example Title')

    def test_event_filter_by_multiple_dates_request(self):
        client = Client()
        query = f"start_date__gte={self.yesterday}&start_date__lte={self.next_week}"
        response = client.get(f'/api/v1/events?{query}')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]['event_name'], 'Example Title')

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
        self.example_event = Event.objects.create(
            event_name='Example title',
            description='Example Description #1',
            featured=False,
        )

    def test_authenticated_event_post_request(self):
        request_data = {
            'event_name': 'Post Event Title',
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
        self.assertEqual(response_data['event_name'], request_data['event_name'])

    def test_unauthenticated_event_post_request(self):
        request_data = {
            'event_name': 'Post Event Title',
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

    def test_authenticated_event_put_request(self):
        request_data = {
            'event_name': 'Post Event Title',
            'description': 'Post Event Description',
            'featured': 'False',
        }
        response = self.client.put(
            f"/api/v1/events/{self.example_event.id}/",
            json.dumps(request_data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.auth_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['event_name'], request_data['event_name'])

    def tearDown(self):
        self.user.delete()
