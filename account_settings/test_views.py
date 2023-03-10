import json

from django.core import mail
from django.test import Client, TestCase
from rest_framework import status


class ContactEmailsTest(TestCase):
    def test_post_index_request_success(self):
        client = Client()
        response = client.post(
            '/api/v1/contact_emails',
            json.dumps({
                'email': 'user@example.com',
                'message': 'That\'s your message body',
                'name': 'Example Username',
                'reference': 'Example reference text',
                'topicType': 'Example topic type',
            }),
            content_type='application/json',
        )
        data = response.json()
        email_body = mail.outbox[0].body
        email_subject = mail.outbox[0].subject
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual('Contact Form Submission', email_subject)
        self.assertIn('email: user@example.com', email_body)
        self.assertIn('message: That\'s your message body', email_body)
        self.assertIn('reference: Example reference text', email_body)
        self.assertIn('topic: Example topic type', email_body)


