from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from concertowl.apis.eventful import get_events_for_artist
from concertowl.apis.wikipedia import get_wikipedia_description
from concertowl.helpers import get_or_none
from concertowl.models import Event, Artist


def _add_artist(name, user=None):
    artist = Artist(name=name)
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


def _add_events(artist_name, location):
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
                            artist_object = _add_artist(artist)
                        event_object.artists.add(artist_object)
                else:
                    if event[key]:
                        setattr(event_object, key, event[key])
            event_object.save()


def index(request):
    return render(request, 'concertowl/index.html')


def events(request):
    events = Event.objects.order_by('-start_time')
    return render(request, 'concertowl/events.html', {'events': events})


class Artists(View):
    def get(self, request, artist=None):
        artists = [artist.to_json() for artist in
                   Artist.objects.filter(subscribers__id=request.user.id).order_by('name')]
        return render(request, 'concertowl/artists.html', {'artists': artists})

    def post(self, request, artist):
        artist_name = artist.lower()
        artistObject = get_or_none(Artist, name=artist_name)
        if artistObject:
            artistObject.subscribers.add(request.user)
            response = {'status': 'Already exists'}
            response.update(artistObject.to_json())
            return JsonResponse(response)

        artist = _add_artist(artist_name, request.user)
        _add_events(artist_name, 'Berlin, Germany')
        response = {'status': 'Created'}
        response.update(artist.to_json())
        return JsonResponse(response)

    def delete(self, request, artist):
        artist = Artist.objects.get(name=artist)
        artist.subscribers.remove(request.user)
        num_deleted = 0
        if not artist.subscribers.count():
            num_deleted, _ = artist.delete()
        return JsonResponse({'deleted': num_deleted})
