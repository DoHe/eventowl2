from concertowl.apis.eventful import get_events_for_artist
from concertowl.apis.wikipedia import get_wikipedia_description
from concertowl.models import Artist, Event, Notification


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def add_artist(name, user=None):
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
        except:
            pass
    artist.save()
    if user:
        artist.subscribers.add(user)
        artist.save()
    return artist


def add_events(artist_name, location):
    print("Adding events...")
    for event in get_events_for_artist(artist_name, location):
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
    filtered = Notification.objects.filter(event__artists__subscribers__id=user_id).order_by('created')
    return [n.to_json() for n in filtered]
