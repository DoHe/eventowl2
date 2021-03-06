import math
import os
from functools import partial
from multiprocessing.pool import Pool

import requests
from django_q.tasks import async_task as async_q
from retrying import retry
from sentry_sdk import capture_exception

from concertowl.apis.events import filter_events, unique_collected_events
from concertowl.helpers import add_event, split_parts
from eventowl.settings import SENTRY_DSN

API_URL = "http://api.eventful.com/json/events/search"
DEFAULT_PARAMS = {'app_key': os.getenv('EVENTFUL_API_KEY'), 'date': 'Future', 'category': 'music'}


def _as_list(obj):
    if not isinstance(obj, list):
        return [obj]
    return obj


def _performers(event):
    if event['performers'] is None:
        return [event['title'].lower()]
    return [p['name'].lower() for p in _as_list(event['performers']['performer'])]


def _as_https(u):
    if u.startswith('http:'):
        return u.replace('http:', 'https:', 1)
    return u


def _event(api_event, performers):
    try:
        return {
            'picture': _as_https(api_event['image']['medium']['url']) if api_event.get('image') else None,
            'city': api_event['city_name'],
            'country': api_event['country_name'],
            'title': api_event.get('title', ', '.join(performers)),
            'start_time': api_event['start_time'],
            'end_time': api_event.get('stop_time'),
            'venue': api_event.get('venue_name'),
            'address': api_event.get('venue_address'),
            'ticket_url': _as_https(api_event['url']),
            'artists': performers
        }
    except KeyError:
        return {}


@retry(wait_fixed=2000, stop_max_attempt_number=10)
def _get_events_page(artists, location, page_number):
    if not page_number % 50:
        print("    Working on page", page_number)
    artists = set(artist.lower for artist in artists)
    resp = requests.get(API_URL, params=dict(location=location, page_number=page_number, **DEFAULT_PARAMS))
    resp.raise_for_status()
    parsed = resp.json()
    if not parsed['events']:
        return []
    events = []
    for event in parsed['events']['event']:
        performers = _performers(event)
        if not set(performers) & artists:
            continue
        model_event = _event(event, performers)
        if model_event:
            events.append(model_event)
    if page_number == 1:
        return events, int(parsed['page_count'])
    else:
        return events


@retry(wait_fixed=2000, stop_max_attempt_number=10)
def _get_events(artist, location=None):
    resp = requests.get(API_URL, params=dict(location=location, keywords=artist, page_size=250, **DEFAULT_PARAMS))
    resp.raise_for_status()
    parsed = resp.json()
    if not parsed.get('events'):
        return []
    events = []
    for event in parsed['events']['event']:
        performers = _performers(event)
        if artist.lower() not in performers:
            continue
        model_event = _event(event, performers)
        if model_event:
            events.append(model_event)
    return events


def _safe_get_events(*args, **kwargs):
    try:
        return _get_events(*args, **kwargs)
    except Exception as e:
        if SENTRY_DSN:
            capture_exception(e)
        return []


def _get_events_for_locations(artists, locations):
    events = []
    for artist in artists:
        events += _get_events(artist)
    return filter_events(events, locations)


def get_events_for_artists_block(artists, location):
    print("Getting events...")
    events, page_count = _get_events_page(artists, location, 1)
    print("    {} pages".format(page_count))
    collected_events = [events]
    with Pool(math.ceil(page_count / 4)) as pool:
        collected_events += pool.map(partial(_get_events_page, artists, location), range(2, page_count + 2))
    print("Done!")
    return unique_collected_events(collected_events)


def get_events_for_artists(artists, locations):
    collected_events = []
    with Pool(min(len(artists), 10)) as pool:
        collected_events += pool.map(_safe_get_events, artists)
    return filter_events(unique_collected_events(collected_events), locations)


def _add_events(task):
    for event in task.result:
        add_event(event)


def add_events_for_artists(artists, locations):
    for artists_part in split_parts(artists, 10):
        async_q(_get_events_for_locations, artists_part, locations, hook='concertowl.apis.eventful._add_events')


def add_events_for_artist(artist_name, location):
    print("Adding events...")
    for event in get_events_for_artist(artist_name, location):
        add_event(event)


def get_events_for_artist(artist, location=None):
    return _get_events(artist, location)
