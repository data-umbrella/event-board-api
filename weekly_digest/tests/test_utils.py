
import datetime
from django.test import TestCase
from weekly_digest.models import WeeklyDigestSubscription
from weekly_digest.utils import trigger_digest_email
from django.core import mail
from events.models import Event

class WeeklyDigestUtilsTest(TestCase):
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
        
        trigger_digest_email()

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
        
        trigger_digest_email()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual('Weekly Digest', mail.outbox[0].subject )

    def test_trigger_digest_email_request_no_events(self):        
        trigger_digest_email()

        self.assertEqual(len(mail.outbox), 0)

