import json
from multiprocessing import Pool
from urllib.parse import quote_plus

import requests
from retrying import retry
from sentry_sdk import capture_exception

from concertowl.apis.events import filter_events, unique_collected_events
from eventowl.settings import SENTRY_DSN

API_URL = 'https://rest.bandsintown.com/artists/{}/events'


def _event(api_event, performers):
    try:
        ticket_url = [offer['url'] for offer in api_event['offers'] if offer['type'] == 'Tickets']
        description = api_event.get('description')
        return {
            'picture': None,
            'city': api_event['venue']['city'],
            'country': api_event['venue']['country'],
            'title': description[:50] if description else ', '.join(p.title() for p in performers),
            'start_time': api_event['datetime'].replace('T', ' '),
            'end_time': None,
            'venue': api_event['venue']['name'],
            'address': None,
            'ticket_url': ticket_url[0] if ticket_url else api_event['url'],
            'artists': performers
        }
    except KeyError:
        return {}


@retry(wait_fixed=60, stop_max_attempt_number=11)
def _get_events_call(artist):
    resp = requests.get(API_URL.format(quote_plus(artist)),
                        params={'app_id': 'eventowl'})
    resp.raise_for_status()
    try:
        return resp.json()
    except json.JSONDecodeError:
        if 'not found' in resp.text.lower():
            return []
        raise IOError(resp.text)


def _get_events(artist):
    try:
        parsed = _get_events_call(artist)
    except Exception as e:
        if SENTRY_DSN:
            capture_exception(e)
        return []
    if not parsed:
        return []
    events = []
    for event in parsed:
        performers = [a.lower() for a in event.get('lineup', [])]
        if artist.lower() not in performers:
            continue
        model_event = _event(event, performers)
        if model_event:
            events.append(model_event)
    return events


def get_events_for_artists(artists, locations):
    collected_events = []
    with Pool(min(len(artists), 5)) as pool:
        collected_events += pool.map(_get_events, artists)
    return filter_events(unique_collected_events(collected_events), locations)
