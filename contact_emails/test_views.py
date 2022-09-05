import json

from django.core import mail
from django.test import Client, TestCase
from rest_framework import status


class ContactEmailsTest(TestCase):
    def test_post_index_request_success(self):
        client = Client()
        response = client.post(
            '/api/v1/contact_emails',
            json.dumps({'email': 'user@example.com', 'message': "That's your message body"}),
            content_type='application/json',
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # # self.assertEqual(data['status'], 'Success')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual('Contact Form Submission', mail.outbox[0].subject)
        self.assertIn('sender: user@example.com', mail.outbox[0].body)
        self.assertIn("message: That's your message body", mail.outbox[0].body)


