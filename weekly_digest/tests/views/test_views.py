import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from weekly_digest.models import WeeklyDigestSubscription


class SubscribeToWeeklyDigestTest(TestCase):
    """ Test module for subscribing to weekly digest """
    
    def setUp(self):
        self.existing_email_address = 'janesmith@example.com'
        self.new_email_address = 'johnsmith@example.com'
        self.weekly_digest_subscription = WeeklyDigestSubscription.objects.create(
            email=self.existing_email_address,
            subscribed=True,
        )

    def test_weekly_digest_post_request(self):
        request_data = {
            'email': self.new_email_address,
            'subscribed': 'True',
        }
        response = self.client.post(
            '/api/v1/weekly_digests',
            json.dumps(request_data),
            content_type="application/json",
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['email'], self.new_email_address)
        self.assertEqual(response_data['subscribed'], True)
    
    def test_weekly_digest_post_request(self):
        request_data = {
            'email': self.new_email_address,
            'subscribed': 'True',
        }
        response = self.client.post(
            '/api/v1/weekly_digests',
            json.dumps(request_data),
            content_type="application/json",
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['email'], self.new_email_address)
        self.assertEqual(response_data['subscribed'], True)

    def test_weekly_digest_put_request(self):
        request_data = {
            'email': self.existing_email_address,
            'subscribed': 'false',
        }
        response = self.client.put(
            f"/api/v1/weekly_digests/{self.weekly_digest_subscription.id}/",
            json.dumps(request_data),
            content_type="application/json",
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['email'], self.existing_email_address)
        self.assertEqual(response_data['subscribed'], False)
    
    def test_weekly_digest_get_request(self):
        response = self.client.get(
            f"/api/v1/weekly_digests/{self.weekly_digest_subscription.id}/",
            content_type="application/json",
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['email'], self.existing_email_address)
        self.assertEqual(response_data['subscribed'], True)
    
    def test_weekly_digest_delete_request(self):
        response = self.client.delete(
            f"/api/v1/weekly_digests/{self.weekly_digest_subscription.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)




