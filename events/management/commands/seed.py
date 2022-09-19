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


def parse_url(raw_url):
    if raw_url.lower() == 'not found':
        return
    else:
        return raw_url


def format_region(raw_string):
   return "-".join(raw_string.lower().split())

LANGUAGE_MAP = {
    "English": "en",
    "Spanish": "es",
}

REGION_MAP = {
    "Online": "online",
    "Canada / USA": "usa-canada",
    "Europe": "europe",
    "Asia": "asia",
    "Africa": "africa",
    "Latin America": "latin-america",
    "Middle East": "middle-east",
    "Oceania": "oceania",
}


def format_language(language_string):
    if language_string == '': return 'en'
    language_string = " ".join(language_string.strip().split())
    languages = language_string.strip().split(',')
    languages = [l for l in languages if l]
    formatted_languages = map(lambda language: LANGUAGE_MAP[language], languages)
    return ",".join(formatted_languages)


def format_region(region_string):
    if (region_string == ''): return None
    return REGION_MAP[region_string]


def create_event(event_data):
    """Creates an events object combining different elements from the list"""

    logger.info("Creating event")

    event = Event(
        event_name=event_data['event_name'],
        description='',
        organization_name=event_data['organization_name'],
        organization_url=event_data['organization_url'],
        featured=event_data['featured'] == '1',
        start_date=event_data['start_date'],
        end_date=event_data['end_date'],
        tags=event_data['tags'],
        event_url=event_data['event_url'],
        image_url=event_data['image_url'],
        code_of_conduct_url=parse_url(event_data['code_of_conduct_url']),
        acronym=event_data['acronym'],
        language=format_language(event_data['language']),
        region=format_region(event_data['region']),
        in_person=coerce_boolean(event_data['in_person']),
        virtual=coerce_boolean(event_data['virtual']),
        hash_tag=event_data['hash_tag'],
        cfp_due_date=coerce_date_field(event_data['cfp_due_date']),
        price=event_data['price'],
        price_range=event_data['price_range'],
        cfp_url=event_data['cfp_url'],
        event_type=event_data['event_type'].lower(),
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


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')