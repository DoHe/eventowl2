import datetime
import json

from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views import View
from django_q.tasks import async_task as async_q

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
        events = events.filter(city__iexact=request.user.profile.city)
        events = events.order_by('start_time').distinct()

        if event_format == 'ical':
            response = HttpResponse(events_to_ical(events), content_type='text/calendar')
            response['Filename'] = 'events.ics'
            response['Content-Disposition'] = 'attachment; filename=events.ics'
            return response

        json_events = [event.to_json() for event in events]
        return render(request, 'concertowl/events.html', {'events': json.dumps(json_events)})


class EventById(View):
    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)
        return render(request, 'concertowl/event_by_id.html', {'events': [event.to_json()]})


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
        return JsonResponse({
            'status': 'ok',
            'notifications': [n.to_json() for n in user_notifications(request.user.id)]
        })

    def post(self, request, action=None):
        if action == 'read':
            ts = request.POST.get('ts')
            if ts:
                ts = datetime.datetime.fromtimestamp(int(ts)/1000)
                notifications = user_notifications(request.user.id).filter(created__lte=ts)
                try:
                    user = User.objects.get(id=request.user.id)
                    for n in notifications:
                        n.read_by.add(user)
                        n.save()
                except User.DoesNotExist:
                    pass
        return JsonResponse({'status': 'ok'})


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
