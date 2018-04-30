import datetime
import json

from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views import View
from django_q.tasks import async as async_q

from concertowl.apis.spotify import add_spotify_artists
from concertowl.helpers import get_or_none, add_artist, add_events, user_notifications, events_to_ical
from concertowl.models import Event, Artist


def index(request):
    return render(request, 'concertowl/index.html')


class Events(View):
    def get(self, request):
        events = Event.objects.filter(start_time__gte=datetime.date.today())
        user_uuid = request.GET.get('uuid')
        format = request.GET.get('format')
        if user_uuid:
            if not format:
                return HttpResponseForbidden("Access forbidden")
            events.filter(artists__subscribers__profile__uuid=user_uuid)
        else:
            events.filter(artists__subscribers__id=request.user.id)
        events.order_by('start_time')

        if format == 'ical':
            response = HttpResponse(events_to_ical(events), content_type='text/calendar')
            response['Filename'] = 'events.ics'
            response['Content-Disposition'] = 'attachment; filename=events.ics'
            return response

        json_events = [event.to_json() for event in events]
        return render(request, 'concertowl/events.html', {'events': json.dumps(json_events)})


class Artists(View):

    def get(self, request, artist=None):
        artists = [artist.to_json() for artist in
                   Artist.objects.filter(subscribers__id=request.user.id).order_by('name')]
        return render(request, 'concertowl/artists.html', {'artists': json.dumps(artists)})

    def post(self, request, artist):
        artist_name = artist.lower()
        artistObject = get_or_none(Artist, name=artist_name)
        if artistObject:
            artistObject.subscribers.add(request.user)
            response = {'status': 'Already exists'}
            response.update(artistObject.to_json())
            return JsonResponse(response)

        artist = add_artist(artist_name, request.user)
        async_q(add_events, artist_name, 'Berlin, Germany')
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


class Notifications(View):

    def get(self, request):
        return JsonResponse({'status': 'ok', 'notifications': user_notifications(request.user.id)})


class Spotify(View):

    def get(self, request):
        code = request.GET.get('code')
        if code is not None:
            async_q(add_spotify_artists, code, request.user)

        return render(request, 'concertowl/spotify.html')
