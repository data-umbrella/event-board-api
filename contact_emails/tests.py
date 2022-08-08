from django.test import TestCase, Client
from rest_framework import status
import json


class EmailsTest(TestCase):
    def test_get_index_request_success(self):
        client = Client()
        response = client.get(
            '/api/v1/contact_emails',
            content_type='application/json',
        )
        json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json['ping'], 'pong')

    def test_post_index_request_success(self):
        client = Client()
        response = client.post(
            '/api/v1/contact_emails',
            json.dumps({'email': 'user@example.com'}),
            content_type='application/json',
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['email'], 'user@example.com')
