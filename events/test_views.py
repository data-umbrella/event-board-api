from django.test import TestCase, Client
from events.models import Event
from rest_framework import status
from django.urls import reverse
import json


class EventAPITest(TestCase):
    """ Test module for Event model """


    def event_title(self):
        return 'Example Title'


    def setUp(self):
        Event.objects.create(
            title=self.event_title(),
            description='Example Description',
            featured=False,
        )


    def test_event_get_request(self):
        client = Client()
        response = client.get('/api/v1/events')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data[0]['title'], self.event_title())


    def test_event_post_request(self):
        client = Client()
        request_data = {
            'title': 'Post Event Title',
            'description': 'Post Event Description',
            'featured': 'False',
        }
        response = client.post(
            '/api/v1/events',
            json.dumps(request_data),
            content_type="application/json",
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['title'], request_data['title'])
