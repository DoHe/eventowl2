from datetime import datetime, timedelta

import icalendar

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
    event_object, new = Event.objects.get_or_create(
        venue=event['venue'],
        city=event['city'],
        start_time=event['start_time']
    )
    if new:
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


def user_notifications(user_id):
    filtered = Notification.objects.filter(
        event__artists__subscribers__id=user_id
    ).exclude(
        read_by__id=user_id
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
        ical_event.add('description', "{} at {}\n\n{}".format(artists, event.venue, event.ticket_url))
        if event.start_time.hour or event.start_time.minute:
            ical_event.add('dtstart', event.start_time)
            if event.end_time:
                ical_event.add('dtend', event.end_time)
            else:
                ical_event.add('dtend', event.start_time + timedelta(hours=2))
        else:
            ical_event.add('dtstart', event.start_time.date())
        if event.address:
            ical_event.add('location', '{}, {}'.format(event.venue, event.address))
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
