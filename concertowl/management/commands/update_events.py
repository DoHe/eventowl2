from django.core.management import BaseCommand

from concertowl.apis.eventful import get_events_for_artists
from concertowl.helpers import add_event
from concertowl.models import Artist, UserProfile


class Command(BaseCommand):
    help = 'Update events for all artists'

    def handle(self, *args, **options):
        artists = [artist.name for artist in Artist.objects.all()]
        locations = {'{},{}'.format(u.city.lower(), u.country.lower()) for u in UserProfile.objects.all()}
        print("Getting events for {} artists in {} locations...".format(len(artists), len(locations)))
        events = list(get_events_for_artists(artists, locations))
        print("Adding {} events...".format(len(events)))
        for event in events:
            add_event(event)
        print("Done")
