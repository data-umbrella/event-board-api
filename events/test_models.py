from django.test import TestCase
from events.models import Event
from django.core.validators import ValidationError


class EventTest(TestCase):
    """ Test module for Event model """

    def test_event_initialization(self):
        event = Event.objects.create(
            event_name='Example Title',
            description='Example Description',
            featured=False,
            organization_name='Example org name',
        )

        event.full_clean()
        event.save()
        self.assertEqual(event.organization_name, 'Example org name')


    def test_event_validations(self):
        event = Event.objects.create(
            event_name=None,
            description='Example Description',
            featured=False,
            organization_name=None,
        )

        with self.assertRaises(ValidationError) as error:
            event.full_clean()

            self.assertEqual(
                error.exception.message_dict['event_name'],
                ['This field cannot be blank.'],
            )
