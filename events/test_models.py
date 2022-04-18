from django.test import TestCase
from .models import Event


class EventTest(TestCase):
    """ Test module for Event model """

    def setUp(self):
        Event.objects.create(
            title='Example Title',
            description='Example Description',
            featured=False,
        )

    def test_event_description(self):
        event = Event.objects.get(title='Example Title')
        self.assertEqual(event.description, "Example Description")
