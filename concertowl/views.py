from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from concertowl.helpers import get_wikipedia_description, get_or_none
from concertowl.models import Event, Artist


def index(request):
    return render(request, 'concertowl/index.html')


def events(request):
    events = Event.objects.order_by('-date_time')
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
        description = url = picture = None
        try:
            description, url, picture = get_wikipedia_description(artist_name)
        except:
            pass
        artist = Artist(name=artist)
        if description:
            artist.description = description
        if url:
            artist.url = url
        if picture:
            artist.picture = picture
        artist.save()
        artist.subscribers.add(request.user)
        artist.save()
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
