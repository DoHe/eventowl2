from django.core.management import BaseCommand

from concertowl.apis.eventful import get_events_for_artists
from concertowl.helpers import add_event
from concertowl.models import Artist, UserProfile


class Command(BaseCommand):
    help = 'Update events for all artists'

    def handle(self, *args, **options):
        artists = [artist.name for artist in Artist.objects.all()]
        locations = {'{},{}'.format(u.city.lower(), u.country.lower()) for u in UserProfile.objects.all()}
        for event in get_events_for_artists(artists, locations):
            add_event(event)
