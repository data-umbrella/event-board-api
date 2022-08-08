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


def create_event(event_data):
    """Creates an events object combining different elements from the list"""
    logger.info("Creating event")
    faker = Faker()
    today = datetime.date.today()
    start_date = event_data['start_date']
    end_date = event_data['end_date']
    description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    organization_name = faker.company()
    title=faker.paragraph(nb_sentences=1)
    tags = random.sample(['python', 'machine-learning', 'data-science'], 1)

    event = Event(
        title=event_data['event_name'],
        description=description,
        organization_name=event_data['organization_name'],
        organization_url=event_data['organization_url'],
        featured=event_data['featured'] == 'True',
        start_date=start_date,
        end_date=end_date,
        tags=event_data['tags'],
        event_url=event_data['event_url'],
    )
    event.save()
    logger.info("{} event created.".format(event))
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


