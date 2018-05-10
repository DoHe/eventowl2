import datetime
import json

from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views import View
from django_q.tasks import async as async_q

from concertowl.apis.eventful import add_events_for_artist
from concertowl.apis.spotify import add_spotify_artists
from concertowl.forms import UserForm
from concertowl.helpers import (add_artist, events_to_ical, get_or_none,
                                user_notifications)
from concertowl.models import Artist, Event


def index(request):
    return render(request, 'concertowl/index.html')


class Events(View):
    def get(self, request):
        events = Event.objects.filter(start_time__gte=datetime.date.today())
        user_uuid = request.GET.get('uuid')
        event_format = request.GET.get('format')
        if user_uuid:
            if not event_format:
                return HttpResponseForbidden("Access forbidden")
            events = events.filter(artists__subscribers__profile__uuid=user_uuid)
        else:
            events = events.filter(artists__subscribers__id=request.user.id)
        events = events.order_by('start_time')

        if event_format == 'ical':
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
        async_q(add_events_for_artist, artist_name, 'Berlin, Germany')
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


class UserPreferences(View):

    def _default_data(self, user):
        return {
            'email': user.email,
            'username': user.username if user.profile.manual else '',
            'password': user.password,
            'city': user.profile.city,
            'country': user.profile.country
        }

    def get(self, request):
        form = UserForm(self._default_data(request.user))
        return render(request, 'concertowl/user_preferences.html', {'form': form})

    def post(self, request):
        default_data = self._default_data(request.user)
        form = UserForm(request.POST, initial=default_data)
        save_user = False
        save_profile = False
        success = ""
        if form.is_valid():
            success = "Nothing changed"
            for field in form.changed_data:
                new_value = request.POST[field]
                if field in ['city', 'country']:
                    setattr(request.user.profile, field, new_value)
                    save_profile = True
                elif field == 'password':
                    if new_value and not check_password(new_value, default_data['password']):
                        request.user.set_password(new_value)
                        save_user = True
                else:
                    setattr(request.user, field, request.POST[field])
                    if field == 'username':
                        request.user.profile.manual = True
                        save_profile = True
                    save_user = True
            if save_profile:
                request.user.profile.save()
            if save_user:
                request.user.save()
                login(request, request.user)
        if save_profile or save_user:
            success = "Changes applied!"
        return render(request, 'concertowl/user_preferences.html', {'form': form, 'success': success})
