import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django_q.tasks import async as async_q

from concertowl.helpers import get_or_none, add_artist, add_events, user_notifications
from concertowl.models import Event, Artist


def index(request):
    return render(request, 'concertowl/index.html')


def events(request):
    events = [event.to_json() for event in
              Event.objects.filter(artists__subscribers__id=request.user.id).order_by('-start_time')]
    return render(request, 'concertowl/events.html', {'events': json.dumps(events)})


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
        return JsonResponse({})
        # if request.GET.get('code') is not None:
        #     code = request.GET.get('code')
        #     token_info = spotify_token_from_code(code)
        #     print(token_info["access_token"])
        #     print(token_info["refresh_token"]
        #     spotify_artists.delay(token_info["access_token"], request.user)
        #     return render(request, 'concertowl/spotify_running.html')
        #
        # return render(request, 'concertowl/spotify.html')
