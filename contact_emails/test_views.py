from django.test import TestCase, Client
from rest_framework import status
import json
from django.core import mail


class ContactEmailsTest(TestCase):
    def test_post_index_request_success(self):
        client = Client()
        response = client.post(
            '/api/v1/contact_emails',
            json.dumps({'email': 'user@example.com', 'message': 'That’s your message body'}),
            content_type='application/json',
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['status'], 'Success')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Contact Form Submission')
        self.assertEqual(mail.outbox[0].body, 'That’s your message body')
