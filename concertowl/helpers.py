from datetime import datetime, timedelta

import icalendar
from textdistance import lcsseq

from concertowl.apis.wikipedia import get_wikipedia_description
from concertowl.models import Artist, Event, Notification


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def add_artist(name, user=None):
    if not name:
        return None
    artist, new = Artist.objects.get_or_create(name=name)
    if new:
        try:
            description, url, picture = get_wikipedia_description(name)
            if description:
                artist.description = description
            if url:
                artist.url = url
            if picture:
                artist.picture = picture
        except Exception:
            pass
        artist.save()
    if user:
        artist.subscribers.add(user)
        artist.save()
    return artist


def add_event(event):
    event_object = get_or_none(
        Event,
        venue=event['venue'],
        city__iexact=event['city'],
        start_time=event['start_time']
    )
    if event_object is None:
        event_object = Event(
            venue=event['venue'],
            city=event['city'],
            start_time=event['start_time']
        )
        event_object.save()
        for key in event:
            if key == 'artists':
                for artist in event[key]:
                    artist_object = get_or_none(Artist, name=artist)
                    if artist_object is None:
                        artist_object = add_artist(artist)
                    event_object.artists.add(artist_object)
            else:
                if event[key]:
                    setattr(event_object, key, event[key])
        event_object.save()
        Notification(event=event_object).save()


def user_notifications(user):
    filtered = Notification.objects.filter(
        event__city__iexact=user.profile.city,
        event__artists__subscribers__id=user.id
    ).exclude(
        read_by__id=user.id
    ).order_by('created')
    return filtered


def events_to_ical(events):
    cal = icalendar.Calendar()
    cal.add('prodid', '-//Eventowl//Concertowl//Global')
    cal.add('version', '2.0')
    for idx, event in enumerate(events):
        ical_event = icalendar.Event()
        ical_event.add('dtstamp', datetime.now())
        now = ical_event['dtstamp']
        ical_event.add('uid', f'{now.to_ical().decode()}/{idx}@Concertowl')
        artists = ', '.join(a.name.title() for a in event.artists.all())
        ical_event.add('description', f"{artists} at {event.venue}")
        if event.start_time.hour or event.start_time.minute:
            ical_event.add('dtstart', event.start_time.replace(tzinfo=None))
            if event.end_time:
                ical_event.add('dtend', event.end_time.replace(tzinfo=None))
            else:
                ical_event.add('dtend', (event.start_time + timedelta(hours=2)).replace(tzinfo=None))
        else:
            ical_event.add('dtstart', event.start_time.date())
        if event.address:
            ical_event.add('location', f'{event.venue}, {event.address}')
        else:
            ical_event.add('location', event.venue)
        ical_event.add('summary', event.title)
        cal.add_component(ical_event)
    return cal.to_ical()


def location(city, country):
    return '{},{}'.format(city.lower(), country.lower())


def split_parts(iterable, num_parts):
    li = list(iterable)
    num_parts = min(num_parts, len(li))
    return [li[i::num_parts] for i in range(num_parts)]


def unique_events(events):
    unique_events = []
    duplicate_indexes = set()
    for left_idx, left_event in enumerate(events):
        if left_idx in duplicate_indexes:
            continue
        for right_idx, right_event in enumerate(events):
            if left_idx == right_idx:
                continue
            if is_same_event(left_event, right_event):
                duplicate_indexes.update({left_idx, right_idx})
                if right_event.created and (right_event.created > left_event.created):
                    left_event = right_event
        unique_events.append(left_event)

    return unique_events


def clean(s):
    return s.lower().strip()


def is_same_event(left_event, right_event):
    left_venue = clean(left_event.venue)
    right_venue = clean(right_event.venue)
    venue_similarity = lcsseq.normalized_similarity(left_venue, right_venue)
    is_similar_venue = venue_similarity > 0.8

    earlier = left_event.start_time - timedelta(hours=2)
    later = left_event.start_time + timedelta(hours=2)
    is_similar_time = earlier <= right_event.start_time <= later

    if is_similar_venue and is_similar_time:
        return True

    is_same_date = left_event.start_time.date() == right_event.start_time.date()
    if is_same_date and are_similar_artists(left_event.artists.all(), right_event.artists.all()):
        return True

    return False


def are_similar_artists(left_artists, right_artists):
    for left_artist in left_artists:
        left_artist = clean(left_artist.name)
        for right_artist in right_artists:
            right_artist = clean(right_artist.name)
            if lcsseq.normalized_similarity(left_artist, right_artist) > 0.8:
                return True
    return False
