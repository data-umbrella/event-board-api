from events.models import Event
from django.db.models.signals import pre_save
from django.dispatch import receiver
from geopy.geocoders import Nominatim


def get_coordinates(location, region):
    geolocator = Nominatim(user_agent='data-umbrella/event-board-api')
    geolocation = geolocator.geocode(f'{location},{region}')
    return (geolocation.latitude, geolocation.longitude)


@receiver(pre_save, sender=Event)
def save_coordinates(sender, instance, **kwargs):
    # import pdb
    # pdb.set_trace()
    coords = get_coordinates(instance.location, instance.region)
    instance.latitude = coords[0]
    instance.longitude = coords[1]
