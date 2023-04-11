import os.path
from django.conf import settings
from django.core.management.base import BaseCommand
import random
from events.models import Event
import logging
from datetime import datetime, timedelta
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

""" Seeds for testing pagination"""
MODE_PAGINATION = 'pagination'


fake = Faker()


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

def parse_social_links(media_data):
    col_names = ['url_linkedin', 'url_twittter', 'url_other']
    links = []
    for col_name in col_names:
        if col_name not in media_data:
            continue

        value = media_data[col_name]
        if value != '':
            links.append({'id': col_name, 'url': value})
    
    return links


LANGUAGE_MAP = {
    "English": "en",
    "Spanish": "es",
    "Portuguese": "pt",
    "French": "fr",
    "Japanese": "jp"
}

REGION_MAP = {
    "Africa": "africa",
    "Asia": "asia",
    "Canada / USA": "canada-usa",
    "Europe": "europe",
    "Latin America": "latin-america",
    "Middle East": "middle-east",
    "Oceania": "oceania",
    "Online": "online",
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

    media_data = [event_data['url_linkedin'], event_data['url_twitter'], event_data['url_other']]

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
        price=event_data['paid_or_free'],
        price_range=event_data['price_range'],
        cfp_url=event_data['cfp_url'],
        event_type=event_data['event_type'].lower(),
        published=True,
        social_media_links=parse_social_links(event_data),
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
    if settings.DEVELOPMENT_MODE:
        clear_data()

    if mode == MODE_CLEAR:
        return

    if mode == MODE_PAGINATION:
        for i in range(0, 200):
            start_date = datetime.strptime('11-19-2022', '%m-%d-%Y')
            start_date = start_date + timedelta(days=i)

            featured = None
            if i < 10:
                featured = '1'

            event_data = {
                'event_name': fake.sentence(nb_words=10),
                'description': fake.sentence(nb_words=10),
                'organization_name': fake.company(),
                'organization_url': 'http://www.example.com',
                'featured': featured,
                'start_date': start_date,
                'end_date': start_date,
                'tags': 'python',
                'event_url': 'http://www.example.com',
                'image_url': None,
                'code_of_conduct_url': 'http://www.example.com',
                'acronym': 'EXP',
                'language': 'English',
                'region': 'Canada / USA',
                'in_person': bool(random.getrandbits(1)),
                'virtual': bool(random.getrandbits(1)),
                'hash_tag': '#exp',
                'cfp_due_date': start_date,
                'price': 'free',
                'price_range': '$$$',
                'paid_or_free': 'free',
                'cfp_url': 'https://example.com',
                'event_type': 'Conference',
            }
            create_event(event_data)
    else:
        with open(f"{settings.BASE_DIR}/data/seeds/events-2023-03-20.csv", newline='') as csvfile:
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
