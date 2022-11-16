import datetime
import json
from django.test import TestCase
from rest_framework import status
from weekly_digest.models import WeeklyDigestSubscription
from django.core import mail
from events.models import Event

class SubscribeToWeeklyDigestTest(TestCase):
    """ Test module for subscribing to weekly digest """
    
    def setUp(self):
        # setup subscriptions        
        self.existing_email_address = 'janesmith@example.com'
        self.new_email_address = 'johnsmith@example.com'
        self.weekly_digest_subscription = WeeklyDigestSubscription.objects.create(
            email=self.existing_email_address,
            subscribed=True,
        )

        # setup event dates
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.next_week = self.today + datetime.timedelta(days=7)
        self.four_weeks = self.today + datetime.timedelta(days=28)
        self.next_month = self.today + datetime.timedelta(days=40)


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

    def test_trigger_digest_email_request_week_events(self):
        Event.objects.create(
            event_name='Today Event',
            description='Example Description #1',
            featured=False,
            start_date=self.today,
            language='en',
            event_type='conference',
            price='one-to-nine',
        )
        Event.objects.create(
            event_name='Week from today event',
            description='Example Description #1',
            featured=False,
            start_date=self.next_week,
            language='en',
            event_type='conference',
            price='one-to-nine',
        )
        Event.objects.create(
            event_name='Event in four weeks',
            description='Example Description #1',
            featured=False,
            start_date=self.four_weeks,
            language='en',
            event_type='conference',
            price='one-to-nine',
        )
        Event.objects.create(
            event_name='Big Event Title',
            description='Big Event Description',
            featured=True,
            published=True,
            start_date=self.yesterday,
            region="europe",
        )
        Event.objects.create(
            event_name='Future Event Title',
            description='Future Event Description',
            featured=False,
            start_date=self.next_month,
        )
        
        response = self.client.get(
            f"/api/v1/trigger_weekly_digests",
        )

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['users_count'], 1)
        self.assertEqual(response_data['events'], ['Today Event', 'Week from today event'])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual('Weekly Digest', mail.outbox[0].subject )

    def test_trigger_digest_email_request_month_events(self):
        Event.objects.create(
            event_name='Event in four weeks',
            description='Example Description #1',
            featured=False,
            start_date=self.four_weeks,
            language='en',
            event_type='conference',
            price='one-to-nine',
        )
        Event.objects.create(
            event_name='Big Event Title',
            description='Big Event Description',
            featured=True,
            published=True,
            start_date=self.yesterday,
            region="europe",
        )
        Event.objects.create(
            event_name='Future Event Title',
            description='Future Event Description',
            featured=False,
            start_date=self.next_month,
        )
        
        response = self.client.get(
            f"/api/v1/trigger_weekly_digests",
        )

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['users_count'], 1)
        self.assertEqual(response_data['events'], ['Event in four weeks'])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual('Weekly Digest', mail.outbox[0].subject )

    def test_trigger_digest_email_request_no_events(self):        
        response = self.client.get(
            f"/api/v1/trigger_weekly_digests",
        )

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['users_count'], 1)
        self.assertEqual(response_data['events'], [])
        self.assertEqual(len(mail.outbox), 0)

