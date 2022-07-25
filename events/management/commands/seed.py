from django.core.management.base import BaseCommand
import random
from events.models import Event
import logging

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


def create_event(num):
    """Creates an events object combining different elements from the list"""
    logger.info("Creating event")
    event = Event(
        title=f"Event #{num}",
        description="Example description",
        organization_name="Example organization name",
        featured=True,
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

    # Creating 15 eventses
    for i in range(15):
        create_event(i)
