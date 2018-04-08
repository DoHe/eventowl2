from django.shortcuts import render

from concertowl.models import Event, Artist


def index(request):
    return render(request, 'concertowl/index.html')


def events(request):
    events = Event.objects.order_by('-date_time')
    return render(request, 'concertowl/events.html', {'events': events})


def artists(request):
    artists = Artist.objects.order_by('name')
    return render(request, 'concertowl/artists.html', {'artists': artists})
