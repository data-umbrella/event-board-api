import os.path
from django.conf import settings
from django.core.management.base import BaseCommand
import random
from events.models import Event
import logging
import datetime
from faker import Faker
import random
import csv

# Get an instance of a logger
logger = logging.getLogger(__name__)

# python manage.py seed --mode=refresh

""" Clear all data and creates events """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    logger.info("Delete event instances")
    Event.objects.all().delete()


def coerce_boolean(value):
    if value == 'Yes': return True
    if value == 'No': return False

    return None


def coerce_date_field(value):
    if value == '': return None

    return value


def create_event(event_data):
    """Creates an events object combining different elements from the list"""

    logger.info("Creating event")

    event = Event(
        event_name=event_data['event_name'],
        description='',
        organization_name=event_data['organization_name'],
        organization_url=event_data['organization_url'],
        featured=event_data['featured'] == 'True',
        start_date=event_data['start_date'],
        end_date=event_data['end_date'],
        tags=event_data['tags'],
        event_url=event_data['event_url'],
        image_url=event_data['image_url'],
        code_of_conduct_url=event_data['code_of_conduct_url'],
        acronym=event_data['acronym'],
        language=event_data['language'],
        region=event_data['region'],
        in_person=coerce_boolean(event_data['in_person']),
        virtual=coerce_boolean(event_data['virtual']),
        hash_tag=event_data['hash_tag'],
        cfp_due_date=coerce_date_field(event_data['cfp_due_date']),
        price=event_data['price'],
        price_range=event_data['price_range'],
        cfp_url=event_data['cfp_url'],
    )

    try:
        event.save()
        logger.info("{} event created.".format(event))
    except:
        logger.info(event_data)

    return event


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear
    :return:
    """
    # Clear data from tables
    clear_data()

    if mode == MODE_CLEAR:
        return

    with open(f"{settings.BASE_DIR}/data/seeds/events.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            create_event(row)
