import math
import os
from functools import partial
from multiprocessing.pool import Pool

import requests
from retrying import retry

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


def _event(api_event, performers):
    return {
        'picture': api_event['image']['medium']['url'] if api_event['image'] else None,
        'city': api_event['city_name'],
        'country': api_event['country_name'],
        'title': api_event['title'],
        'start_time': api_event['start_time'],
        'end_time': api_event['stop_time'],
        'venue': api_event['venue_name'],
        'address': api_event['venue_address'],
        'ticket_url': api_event['url'],
        'artists': performers
    }


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
        events.append(_event(event, performers))
    if page_number == 1:
        return events, int(parsed['page_count'])
    else:
        return events


@retry(wait_fixed=2000, stop_max_attempt_number=10)
def _get_events(artist, location=None):
    resp = requests.get(API_URL, params=dict(location=location, keywords=artist, page_size=250, **DEFAULT_PARAMS))
    resp.raise_for_status()
    parsed = resp.json()
    if not parsed['events']:
        return []
    events = []
    for event in parsed['events']['event']:
        performers = _performers(event)
        if artist.lower() not in performers:
            continue
        events.append(_event(event, performers))
    return events


def _unique_events(collected_events):
    ret = {}
    for events in collected_events:
        for event in events:
            ret[event['title'] + event['start_time'] + event['venue']] = event
    return list(ret.values())


def get_events_for_artists_block(artists, location):
    print("Getting events...")
    events, page_count = _get_events_page(artists, location, 1)
    print("    {} pages".format(page_count))
    collected_events = [events]
    with Pool(math.ceil(page_count / 4)) as pool:
        collected_events += pool.map(partial(_get_events_page, artists, location), range(2, page_count + 2))
    print("Done!")
    return _unique_events(collected_events)


def get_events_for_artists(artists, locations):
    collected_events = []
    with Pool(math.ceil(len(artists) / 4)) as pool:
        collected_events += pool.map(_get_events, artists)
    for event in _unique_events(collected_events):
        location = '{},{}'.format(event['city'].lower(), event['country'].lower())
        if location in locations:
            yield event


def get_events_for_artist(artist, location=None):
    return _get_events(artist, location)
